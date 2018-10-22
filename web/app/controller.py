import DB

def getStrategy():
    return DB.getStrategy()

def startStartStrategy():
    return ''

def loadLogList(creator):
    return DB.getStrategyLogList(creator)

def getLogDetail(stratgyLogId):
    return DB.getLogDetail(stratgyLogId)
