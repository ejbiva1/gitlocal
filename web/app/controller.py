import DB

def getStrategy():
    return DB.getStrategy()
#启动策略
def startStartStrategy(strategyId,initBalance,startDate,endDate):
    return ''
#查询历史列表
def loadLogList(creator):
    # creator 是指用户的用户名； 需要我创建一个session
    return DB.getStrategyLogList(creator)
#查询历史账户列表
def getLogDetail(stratgyLogId, creator):
    return DB.getLogDetail(stratgyLogId, creator)
