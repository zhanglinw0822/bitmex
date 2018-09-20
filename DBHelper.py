import pymongo


def getCol(colName):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db_bitmex = client["bitmex"]
    col_order = db_bitmex[colName]
    return col_order


def insert(colName, order):
    # 新增
    # order = { "market": "1", "symbol": "XBTUSD", "ordertype": "B", "orderpricetype" : "S1" , "orderqty" : 800 }
    insert_result = getCol(colName).insert_one(order)
    print(insert_result.inserted_id)


def query(colName, query):
    # 查询
    # query = { "symbol": "XBTUSD" }
    if not query is None:
        doc = getCol(colName).find()
    else:
        doc = getCol(colName).find(query)
    for x in doc:
        print(x)


def modify(colName, query, newvalues):
    # 修改
    # query = { "symbol": "XBTUSD" }
    # newvalues = {"$set": {"orderqty": 1000}}
    getCol(colName).update_one(query, newvalues)
    for x in getCol(colName).find():
        print(x)


def delete(colName, query):
    # 删除
    # query = { "symbol": "XBTUSD" }
    getCol(colName).delete_many(query)
    for x in getCol(colName).find():
        print("delete result:" + x)


if __name__ == "__main__":
    colName = "order"
    order = {"market": "1", "symbol": "XBTUSD", "ordertype": "B", "orderpricetype": "S1", "orderqty": 800}
    insert(colName, order)
    q = {"symbol": "XBTUSD"}
    query(colName, q)
    q = {"symbol": "XBTUSD"}
    newvalues = {"$set": {"orderqty": 1000}}
    modify(colName, q, newvalues)
    delete(colName, q)
