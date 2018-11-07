import DB
import sys
sys.path.append("../..")
import strategy.main as strategyTool



def getStrategy():
    return DB.getStrategy()
#启动策略
def startStartStrategy(strategyId,initBalance,startDate,endDate):
    if (strategyId==1):
        strategyTool.strategy_combination_a(startDate,endDate,initBalance)
    elif (strategyId==2):
        strategyTool.strategy_combination_b(startDate, endDate, initBalance)
    return "好像启动了"
def saveStrategyConf(strategyId,userId,initBalance,startDate,endDate,strategyConfItemlist):
    strategyConfId = DB.saveStrategyConf(userId,strategyId)
    for item in strategyConfItemlist:
        DB.saveStrategyConfItem(item.strategy_conf_id,item.index_label,item.formular,item.price)
    return strategyTool.strategy_poc(strategyId, userId, startDate, endDate, initBalance)
#查询历史列表
def loadLogList(creator):
    # creator 是指用户的用户名； 需要我创建一个session
    return DB.getStrategyLogList(creator)
#查询历史账户列表
def getLogDetail(stratgyLogId, creator):
    return DB.getLogDetail(stratgyLogId, creator)
