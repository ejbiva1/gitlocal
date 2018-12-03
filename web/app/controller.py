import DB
import sys

sys.path.append("../..")
import strategy.main as strategyTool
from facilties.functional import ResponseModel


def getStrategy():
    return DB.getStrategy()


# 启动策略
def startStartStrategy(strategyId, initBalance, startDate, endDate):
    if (strategyId == 1):
        strategyTool.strategy_combination_a(startDate, endDate, initBalance)
    elif (strategyId == 2):
        strategyTool.strategy_combination_b(startDate, endDate, initBalance)
    return "好像启动了"


# 检查是否有重名的策略，True已存在，False不存在
def checkStrategyName(strategy_name, creator):
    is_strategy_name_exist = DB.checkStrategyName(strategy_name, creator)
    response = ResponseModel(is_strategy_name_exist, '1', 'success')
    return response


# 保存策略并执行策略
def saveStrategyAndRun(strategy_name, userId, coin_category, initBalance, startDate, endDate, strategyConfItemlist):
    result = {'status': 0, 'error_message': "", "strategy_id": 0}
    if (DB.checkStrategyName(strategy_name)):
        result['status'] = -1
        result['error_message'] = "策略名称重复"
        return result
    strategyId = DB.saveStrategy(strategy_name, userId, coin_category, initBalance, startDate, endDate)
    for item in strategyConfItemlist:
        DB.saveStrategyConfItem(item['strategy_id'], item['index_label'], item['formular'], item['price'])
    strategyTool.strategy_poc(strategyId, userId, startDate, endDate, initBalance)
    result['strategy_id'] = strategyId
    return result


# 保存策略
def saveStrategy(strategy_name, userId, coin_category, initBalance, startDate, endDate, strategyConfItemlist):
    result = {'status': 0, 'error_message': "", "strategy_id": 0}
    if (DB.checkStrategyName(strategy_name)):
        result['status'] = -1
        result['error_message'] = "策略名称重复"
        return result
    strategyId = DB.saveStrategy(strategy_name, userId, coin_category, initBalance, startDate, endDate)
    for item in strategyConfItemlist:
        DB.saveStrategyConfItem(item['strategy_id'], item['index_label'], item['formular'], item['price'])

    result['strategy_id'] = strategyId
    return result


# 保存策略名称
def saveStrategyName(strategy_id, strategy_name, creator):
    save_strategy_name = DB.saveStrategyName(strategy_id, strategy_name, creator)
    response = ResponseModel(data=save_strategy_name, code='1', message='success')
    return response;


# 查询历史列表
def loadLogList(creator):
    # creator 是指用户的用户名； 需要我创建一个session
    return DB.getStrategyLogList(creator)


# 查询历史账户列表
def getLogDetail(stratgyLogId, creator):
    return DB.getLogDetail(stratgyLogId, creator)


# 查询历史账户列表
def deleteStrategyById(strategyId):
    return DB.deleteStrategyById(strategyId)


# 查询策略列表
def getALLStrategy(creator):
    return DB.getALLStrategy(creator);


# 查询策略详情
def getStrategy(creator, strategyId):
    return DB.getStrategy(creator, strategyId)


# 删除strategy_log
def deleteStrategyLogById(strategy_log_id):
    DB.deleteStrategyLogById(strategy_log_id)
    response = ResponseModel(data='', code='1', message='success')
    return response
