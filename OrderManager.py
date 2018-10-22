import datetime
import logging
import time

from watchdog.observers import Observer

import DBHelper
import FileEventHandler
import FileHelper
import bitmex
import Logger
from send_mail import send_email


def scanorder(strategy):
    path = strategy.get('path')
    files = []
    FileHelper.listdir(path, files)
    for file in files:
        if (FileHelper.getext(file) == 'txt'):
            nowTime = lambda: int(round(time.time() * 1000))
            content = FileHelper.read_one_line(file)

            create_order(strategy, content)

            # DBHelper.query("order", None)
            bakPath = path + "/bak/";
            FileHelper.create(bakPath)
            filename = FileHelper.getbasename(file);
            FileHelper.copy(file, bakPath + filename + "_" + str(nowTime()) + ".txt")


def create_order(strategy, content):
    cols = content.split(" ")

    ordertype = cols[2]
    symbol = cols[1]
    orderQty = cols[4]
    side = None
    if ordertype == 'V':
        side = 'Buy'
    if ordertype == 'X':
        side = 'Sell'
    if ordertype == 'Y':
        side = 'Buy'
    if ordertype == 'W':
        side = 'Sell'
    if ordertype == 'Q':
        side = 'Buy'
    if ordertype == 'P':
        side = 'Sell'
    if ordertype == 'B':
        side = 'Buy'
    if ordertype == 'S':
        side = 'Sell'
    for account in strategy.get('accounts'):
        print('account:'+str(account))
        logger = Logger('all.log', level='debug')
        try:
            client = bitmex.bitmex(test=False, api_key=account.get('key'), api_secret=account.get('secret'))
            # client = bitmex.bitmex(test=True, api_key=account.get('key'), api_secret=account.get('secret'))
            orderresult = client.Order.Order_new(symbol=symbol, orderQty=orderQty, side=side, ordType='Market').result()
        except Exception as e:
            if e.response is None:
                raise e

            # 401 - Auth error. This is fatal.
            if e.response.status_code == 401:
                logger.error("API Key or Secret incorrect, please check and restart.")
                logger.error("Error: " + e.response.text)
                # Always exit, even if rethrow_errors, because this is fatal
                send_email(e.response.text)
                exit(1)

            # 404, can be thrown if order canceled or does not exist.
            elif e.response.status_code == 404:
                send_email(e.response.text)
                exit(1)

            # 429, ratelimit; cancel orders & wait until X-RateLimit-Reset
            elif e.response.status_code == 429:
                logger.error("Ratelimited on current request. Sleeping, then trying again. Try fewer " +
                             "order pairs or contact support@bitmex.com to raise your limits. ")

                # Figure out how long we need to wait.
                ratelimit_reset = e.response.headers['X-RateLimit-Reset']
                to_sleep = int(ratelimit_reset) - int(time.time())
                reset_str = datetime.datetime.fromtimestamp(int(ratelimit_reset)).strftime('%X')

                # We're ratelimited, and we may be waiting for a long time. Cancel orders.
                logger.warning("Canceling all known orders in the meantime.")

                logger.error("Your ratelimit will reset at %s. Sleeping for %d seconds." % (reset_str, to_sleep))
                time.sleep(to_sleep)

            # 503 - BitMEX temporary downtime, likely due to a deploy. Try again
            elif e.response.status_code == 503:
                logger.warning("Unable to contact the BitMEX API (503), retrying. ")
                time.sleep(3)

            elif e.response.status_code == 400:
                error = e.response.json()['error']
                message = error['message'].lower() if error else ''
                if 'insufficient available balance' in message:
                    logger.error('Account out of funds. The message: %s' % error['message'])
                    send_email(e.response.text)
                    exit(1)

        order = {'market': cols[0], 'symbol': symbol, 'ordertype': ordertype, 'orderpricetype': cols[3],
                 'orderqty': orderQty, 'strategyname': strategy.get('name'),'name': account.get('accountname'), 'orderid': orderresult[0]['orderID'], 'createtime': datetime.datetime.now()}
        DBHelper.insert("order", order)
        print('account:' + str(account) + ',order:' + str(order))


def addOrderObserver(strategy):
    observer = Observer()
    event_handler = FileEventHandler.FileEventHandler()
    FileHelper.create(strategy.get('path'))
    observer.schedule(event_handler, strategy.get('path'), True)
    observer.start()
    try:
        while True:
            try:
                time.sleep(1)
                scanorder(strategy)
            except Exception as e:
                print('except:', e)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
