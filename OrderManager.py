import datetime
import time

from watchdog.observers import Observer

import DBHelper
import FileEventHandler
import FileHelper
import bitmex


def scanorder(strategy):
    path = strategy.get('path')
    files = []
    FileHelper.listdir(path, files)
    for file in files:
        nowTime = lambda: int(round(time.time() * 1000))
        content = FileHelper.read_one_line(file)

        create_order(strategy, content)

        # DBHelper.query("order", None)
        bakPath = path + "/bak/";
        FileHelper.create(bakPath)
        FileHelper.copy(file, bakPath + file.replace(path, "") + str(nowTime()) + ".txt")


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
    client = bitmex.bitmex(api_key=strategy.get('key'), api_secret=strategy.get('secret'))
    orderresult = client.Order.Order_new(symbol=symbol, orderQty=orderQty, side=side, ordType='Market').result()
    order = {'market': cols[0], 'symbol': symbol, 'ordertype': ordertype, 'orderpricetype': cols[3],
             'orderqty': orderQty, 'name': strategy.get('name'), 'orderid': orderresult[0]['orderID'], 'createtime': datetime.datetime.now()}
    DBHelper.insert("order", order)


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
