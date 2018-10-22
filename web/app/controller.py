import DB

def getStrategy():
    return DB.getStrategy()
#启动策略
def startStartStrategy(strategyId,initBalance,startDate,endDate):
    return ''
#查询历史列表
def loadLogList(creator):
    return DB.getStrategyLogList(creator)
#查询历史账户列表
def getLogDetail(stratgyLogId):
    return DB.getLogDetail(stratgyLogId)
