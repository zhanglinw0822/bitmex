import threading
import xml.etree.ElementTree as ET
import os
import sys
import OrderManager


# 遍历xml文件
def traverseXml(element):
    # print (len(element))
    if len(element) > 0:
        for child in element:
            print(child.tag, "----", child.attrib)
            traverseXml(child)
    # else:
    # print (element.tag, "----", element.attrib)

def initStrategy(strategys):
    for strategy in strategys:
        print(strategy.get('path') + "," +strategy.get('key')+ "," +strategy.get('secret')+ "," +strategy.get('name'))
        t = threading.Thread(target=OrderManager.addOrderObserver,args=(strategy,), name=strategy.get('name'))
        t.start()


if __name__ == '__main__':
    xmlFilePath = os.path.abspath("D:\strategy\config.xml")
    print(xmlFilePath)
    try:
        tree = ET.parse(xmlFilePath)
        print("tree type:", type(tree))

        # 获得根节点
        root = tree.getroot()
    except Exception as e:  # 捕获除与程序退出sys.exit()相关之外的所有异常
        print("parse test.xml fail!")
        print(e)
        sys.exit()
    #print("root type:", type(root))
    #print(root.tag, "----", root.attrib)

    # 遍历root的下一层
    #for child in root:
    #    print("遍历root的下一层", child.tag, "----", child.attrib)

    # 使用下标访问
    #print(root[0].text)
    #print(root[1][1][0].text)

    #print(20 * "*")
    # 遍历xml文件
    #traverseXml(root)
    #print(20 * "*")

    # 根据标签名查找root下的所有标签
    strategyList = root.findall("strategy")  # 在当前指定目录下遍历
    #print(len(strategyList))

    strategys = []

    for strategy in strategyList:
        path = None
        key = None
        secret = None
        name = None
        for child in strategy:
            print(child.tag, child.text)
            if child.tag == 'path':
                path = child.text
            if child.tag == 'key':
                key = child.text
            if child.tag == 'secret':
                secret = child.text
            if child.tag == 'name':
                name = child.text

        strategys.append({'path':path,'key':key,'secret':secret,'name':name})
    initStrategy(strategys)