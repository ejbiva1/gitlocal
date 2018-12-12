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
def saveStrategyAndRun(strategy_name, userId, coin_category, init_balance, start_time, end_time, strategyConfItemlist):
    result = {'status': 0, 'error_message': "", "strategy_id": 0}
    if (DB.checkStrategyName(strategy_name, userId)):
        result['status'] = -1
        result['error_message'] = "策略名称重复"
        return result
    strategyId = DB.saveStrategy(strategy_name, userId, coin_category, init_balance, start_time, end_time)
    for item in strategyConfItemlist:
        DB.saveStrategyConfItem(strategyId, item['index_label'], item['formular'], item['price'], item['direction'])
    response = strategyTool.strategy_poc(strategyId, start_time, end_time, init_balance)
    result['strategy_id'] = strategyId
    print(response)
    result['response'] = response.__dict__
    return result


# 保存策略
def saveStrategy(strategy_name, userId, coin_category, initBalance, startDate, endDate, strategyConfItemlist):
    result = {'status': 0, 'error_message': "", "strategy_id": 0}
    if (DB.checkStrategyName(strategy_name)):
        result['status'] = -1
        result['error_message'] = "策略名称重复"
        return result

    strategyId = DB.saveStrategy(strategy_name, userId, coin_category, initBalance, startDate, endDate)
    print(strategyId)
    for item in strategyConfItemlist:
        DB.saveStrategyConfItem(strategyId, item['index_label'], item['formular'], item['price'], item['direction'])

    result['strategy_id'] = strategyId
    return result


# 保存策略名称
def saveStrategyName(strategy_id, strategy_name, creator):
    save_strategy_name = DB.saveStrategyName(strategy_id, strategy_name, creator)
    response = ResponseModel(data=save_strategy_name, code='1', message='success')
    return response;


# 查询历史列表
def loadLogList(creator, strategy_id):
    # creator 是指用户的用户名； 需要我创建一个session
    if strategy_id != 0:
        result = DB.getStrategyLogsByStrategyId(creator, strategy_id)

        return result
    # 查询历史账户列表
    return DB.getStrategyLogList(creator)


def getLogDetail(stratgyLogId, creator):
    return DB.getLogDetail(stratgyLogId, creator)


# 删除某条策略 这个最后再测试；
def deleteStrategyById(strategyId):
    return DB.deleteStrategyById(strategyId)


# 查询策略列表， 获取所有策略
def getALLStrategy(creator):
    return DB.getALLStrategy(creator);


# 查询某个策略
def getStrategyDetail(creator, strategy_id):
    strategy = DB.getStrategyDetail(creator, strategy_id);
    response = ResponseModel(data=strategy.__dict__, code='1', message='success')
    return response;


# 查询策略详情
def getStrategy(creator, strategyId):
    strategy_conf_list = []

    result = DB.getStrategy(creator, strategyId)
    strategy_confs = result.__dict__

    # result 此时是个字典， 所以就这个来讲， 字典调用方式是 ['']
    for strategy_conf in strategy_confs['strategy_conf_items']:
        strategy_conf_list.append(strategy_conf.__dict__)

    strategy_confs['strategy_conf_items'] = strategy_conf_list

    response = ResponseModel(data=strategy_confs, code='1', message='success')
    return response;


# 删除strategy_log
def deleteStrategyLogById(strategy_log_id):
    DB.deleteStrategyLogById(strategy_log_id)
    response = ResponseModel(data='', code='1', message='success')
    return response


# 暂存策略
def saveStrategy(strategy_name, userId, strategy_id, coin_category, init_balance, start_time, end_time,
                 strategyConfItemlist):
    result = {'status': 0, 'error_message': "", "strategy_id": 0}
    if (DB.checkStrategyName(strategy_name, userId) and strategy_id == 0):
        result['status'] = -1
        result['error_message'] = "策略名称重复"
        return result

    # strategy_id == 0 , 新增策略 以及 保存 相应条件配置
    if (strategy_id == 0):
        strategyId = DB.saveStrategy(strategy_name, userId, coin_category, init_balance, start_time, end_time)
        print(strategyId)
        for item in strategyConfItemlist:
            DB.saveStrategyConfItem(strategyId, item['index_label'], item['formular'], item['price'],
                                    item['direction'])

        result['strategy_id'] = strategyId
        return result

    # strategy_id != 0 , 执行更新逻辑
    else:
        # 执行更新策略逻辑
        DB.updateStrategy(strategy_id, strategy_name, userId, coin_category, init_balance, start_time, end_time)
        # 执行更新 strategy conf list
        DB.updateStrategyConf(strategy_id)
        for item in strategyConfItemlist:
            DB.saveStrategyConfItem(strategy_id, item['index_label'], item['formular'], item['price'],
                                    item['direction'])

    return result


# 直接执行策略
def executeStrategy(userId, strategy_id):
    # 查询策略基本配置
    strategy_base_info = DB.getStrategyDetail(userId=userId, strategy_id=strategy_id)
    response = strategyTool.strategy_poc(strategy_id, strategy_base_info.start_time, strategy_base_info.end_time,
                                         strategy_base_info.init_balance)

    result = ResponseModel(data=response, code='1', message='success')
    return result


# mobile 执行策略
def mob_executeStrategy(userId, strategy_id, start_time, end_time, coin_category, init_balance):
    # 更新策略
    DB.mob_updateStrategy(userId=userId, strategy_id=strategy_id, start_time=start_time, end_time=end_time,
                          coin_category=coin_category, init_balance=init_balance)

    # 执行策略
    result = strategyTool.strategy_poc(strategy_id=strategy_id, start_time=start_time, end_time=end_time,
                                       init_balance=init_balance)

    # 策略基本信息
    strategy_info = DB.getStrategyDetail(creator=userId, strategy_id=strategy_id)

    data = { 'regression_result': result.__dict__ , 'strategy_info': strategy_info.__dict__}


    response =ResponseModel(data=data, code = '0', message='success')
    print(response)
    return response
