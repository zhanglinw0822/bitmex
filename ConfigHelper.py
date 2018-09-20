import ConfigParser

cf=ConfigParser.ConfigParser()
cf.read("config.ini")

def getConfig(sectionname,key):

    return cf.get(sectionname,key)

if __name__ == "__main__":
    print(getConfig("baseconf","test"))
    print(getConfig("db", "uri"))
