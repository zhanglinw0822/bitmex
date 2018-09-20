import DBHelper
import FileEventHandler
import FileHelper
import time
import datetime
import bitmex

from watchdog.observers import Observer

def scanorder(strategy):
    path = strategy.get('path')
    files = []
    FileHelper.listdir(path, files)
    for file in files:
        nowTime = lambda: int(round(time.time() * 1000))
        content = FileHelper.read_one_line(file)

        create_order(strategy,content)

        DBHelper.query("order", None)
        bakPath = path +"/bak/";
        FileHelper.create(bakPath)
        FileHelper.copy(file, bakPath +file.replace(path, "")+str(nowTime())+".txt")


def create_order(strategy,content):
    cols = content.split(" ")

    #client = bitmex.bitmex(api_key=strategy.get('key'),api_secret=strategy.get('secret'))
    #价格需要获取
    #client.Order.Order_new(symbol=cols[1], orderQty=cols[4], side=Buy, ordType=Market).result()

    order = {'market': cols[0], 'symbol': cols[1], 'ordertype': cols[2], 'orderpricetype': cols[3], 'orderqty': cols[4]
        , 'name': strategy.get('name'), 'orderid':'', 'createtime': datetime.datetime.now()}
    DBHelper.insert("order", order)

def addOrderObserver(strategy):
    observer = Observer()
    event_handler = FileEventHandler.FileEventHandler()
    FileHelper.create(strategy.get('path'))
    observer.schedule(event_handler, strategy.get('path'), True)
    observer.start()
    try:
        while True:
            time.sleep(1)
            scanorder(strategy)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()