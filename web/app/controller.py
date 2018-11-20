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

#检查是否有重名的策略，True已存在，False不存在
def checkStrategyName(strategy_name):
    return DB.checkStrategyName(strategy_name)

#保存策略并执行策略
def saveStrategyAndRun(strategy_name,userId,coin_category,initBalance,startDate,endDate,strategyConfItemlist):
    result ={'status':0,'error_message':"","strategy_id":0}
    if (DB.checkStrategyName(strategy_name)):
        result['status']=-1
        result['error_message']="策略名称重复"
        return result
    strategyId = DB.saveStrategy(strategy_name,userId,coin_category,initBalance,startDate,endDate)
    for item in strategyConfItemlist:
        DB.saveStrategyConfItem(item['strategy_id'],item['index_label'],item['formular'],item['price'])
    strategyTool.strategy_poc(strategyId, userId, startDate, endDate, initBalance)
    result['strategy_id'] = strategyId
    return result

#保存策略
def saveStrategy(strategy_name,userId,coin_category,initBalance,startDate,endDate,strategyConfItemlist):
    result ={'status':0,'error_message':"","strategy_id":0}
    if (DB.checkStrategyName(strategy_name)):
        result['status']=-1
        result['error_message']="策略名称重复"
        return result
    strategyId = DB.saveStrategy(strategy_name,userId,coin_category,initBalance,startDate,endDate)
    for item in strategyConfItemlist:
        DB.saveStrategyConfItem(item['strategy_id'],item['index_label'],item['formular'],item['price'])

    result['strategy_id'] = strategyId
    return result
#保存策略名称
def saveStrategyName(strategy_id,strategy_name,creator):
    return DB.saveStrategyName(strategy_id,strategy_name,creator)

#查询历史列表
def loadLogList(creator):
    # creator 是指用户的用户名； 需要我创建一个session
    return DB.getStrategyLogList(creator)
#查询历史账户列表
def getLogDetail(stratgyLogId, creator):
    return DB.getLogDetail(stratgyLogId, creator)



