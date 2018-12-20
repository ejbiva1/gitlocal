import DB
import sys
from marshmallow import Schema, fields

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
def checkStrategyName(strategy_name, creator, strategy_id):
    is_strategy_name_exist = DB.checkStrategyName(strategy_name, creator)
    if is_strategy_name_exist is True:
        strategy_name_exist = {'exist': is_strategy_name_exist}
        response = ResponseModel(data=strategy_name_exist, code='1', message='策略名称已存在')
        return response
    else:
        strategy_name_exist = {'exist': is_strategy_name_exist}
        response = ResponseModel(data=strategy_name_exist, code='1', message='策略名称未存')
        return response


# 保存策略并执行策略
def saveStrategyAndRun(strategy_id, strategy_name, userId, coin_category, init_balance, start_time, end_time,
                       strategyConfItemlist, strategy_oper):
    result = isExistsStrategyName(strategy_id=strategy_id, strategy_name=strategy_name, userId=userId,
                                  strategy_oper=strategy_oper).__dict__
    print(result)

    if result['data']['strategy_name_exists'] is not True:
        response = strategyOperation(strategy_id, strategy_name, userId, coin_category, init_balance, start_time,
                                     end_time,
                                     strategyConfItemlist, strategy_oper)
        return response
    else:
        response = ResponseModel(data=result, code='1', message="success")
        return response


# 暂存策略(这个也同时执行  新增策略 => 新添加策略 )

def saveStrategy(strategy_id, strategy_name, userId, coin_category, init_balance, start_time, end_time,
                 strategyConfItemlist, strategy_oper):
    # 新增策略 以及保存相应条件
    result = isExistsStrategyName(strategy_id=strategy_id, strategy_name=strategy_name, userId=userId,
                                  strategy_oper=strategy_oper).__dict__
    if result['data']['strategy_name_exists'] is not True:
        strategyId = DB.saveStrategy(strategy_name, userId, coin_category, init_balance, start_time, end_time)
        for item in strategyConfItemlist:
            DB.saveStrategyConfItem(strategyId, item['index_label'], item['formular'], item['price'],
                                    item['direction'])

        response = ResponseModel(data=strategyId, code="1", message="success")
        return response  # 更新策略 =》 更新已存在策略； 首先先判断当前策略名 是否更改；
    else:
        response = ResponseModel(data=result, code="1", message="success")
        return response


def updateStrategy(strategy_name, userId, strategy_id, coin_category, init_balance, start_time, end_time,
                   strategy_oper):
    result = isExistsStrategyName(strategy_id=strategy_id, strategy_name=strategy_name, userId=userId,
                                  strategy_oper=strategy_oper).__dict__
    print(result)
    if result['data']['strategy_name_exists'] is not True:
        strategy_id = DB.updateStrategy(strategy_id, strategy_name, userId, coin_category, init_balance, start_time,
                                        end_time)
        # strategy_id, strategy_name, creator, coin_category, init_balance, start_time, end_time

        # strategy_name, coin_category, init_balance, start_time, end_time, strategy_id, creator

        response = ResponseModel(data=strategy_id, code='1', message='success')
        return response
    else:
        # 执行更新策略逻辑
        response = ResponseModel(data=result, code='1', message='success')
        return response


def saveStrategyConfOrUpdate(strategy_id, strategy_name, userId, coin_category, init_balance, start_time, end_time,
                             strategyConfItemlist, strategy_oper):
    # 在执行保存策略前， 已经判断当前策略名字是否已存在；
    # 新增策略 以及保存相应条件
    if strategy_id == 0 or strategy_oper == 'submit':
        response = saveStrategy(strategy_id=strategy_id, strategy_name=strategy_name, userId=userId,
                                coin_category=coin_category,
                                init_balance=init_balance,
                                start_time=start_time, end_time=end_time,
                                strategyConfItemlist=strategyConfItemlist, strategy_oper=strategy_oper)
        print("save Strategy")
        return response
    elif strategy_oper == 'save':
        response = updateStrategy(strategy_name=strategy_name, userId=userId, strategy_id=strategy_id,
                                  coin_category=coin_category,
                                  init_balance=init_balance, start_time=start_time, end_time=end_time,
                                  strategy_oper=strategy_oper)
        print("update Strategy")
        return response


# update Strategy ; save Strategy
def strategyOperation(strategy_id, strategy_name, userId, coin_category, init_balance, start_time, end_time,
                      strategyConfItemlist, strategy_oper):
    if strategy_oper == "save":
        # update 并且更新
        print("strategyOperation: update Strategy")
        updateStrategy(strategy_id=strategy_id, strategy_name=strategy_name, userId=userId, coin_category=coin_category,
                       init_balance=init_balance, start_time=start_time, end_time=end_time, strategy_oper=strategy_oper)

    elif strategy_oper == "submit":
        print("strategyOperation: Save Strategy")
        # strategy_id, strategy_name, userId, coin_category, init_balance, start_time, end_time,
        # strategyConfItemlist, strategy_oper
        result = saveStrategy(strategy_id=strategy_id, strategy_name=strategy_name, userId=userId,
                              coin_category=coin_category,
                              init_balance=init_balance, start_time=start_time, end_time=end_time,
                              strategyConfItemlist=strategyConfItemlist, strategy_oper=strategy_oper)
        strategy_id = result.data

    strategy_base_info = DB.getStrategyDetail(userId, strategy_id)

    response = {
        "strategy_base_info": strategy_base_info.__dict__
    }

    response = ResponseModel(data=response, code="1", message="success")

    print(response)
    return response

    # 判断一个策略名称是否存在:


def isExistsStrategyName(strategy_id, strategy_name, userId, strategy_oper):
    if strategy_id == 0 or strategy_oper == "submit":
        strategy_name_exists = DB.checkStrategyName(strategy_name=strategy_name, creator=userId)
        result = {
            "strategy_name_exists": strategy_name_exists,
            "strategy_id": strategy_id
        }

        response = ResponseModel(data=result, code='1', message="策略名称重复")
        return response
    elif DB.checkPreviousStrategyName(strategy_id=strategy_id, strategy_name=strategy_name,
                                      creator=userId) is False:
        strategy_name_exists = DB.checkStrategyName(strategy_name=strategy_name, creator=userId)

        result = {
            "strategy_name_exists": strategy_name_exists,
            "strategy_id": strategy_id
        }
        result = ResponseModel(data=result, code='1', message='策略名称重复')
        return result
    else:
        # 若 返回值为true 则说明 此时 策略名称未改变，可以继续完成
        result = {
            "strategy_name_exists": False,
            "strategy_id": strategy_id
        }

        result = ResponseModel(data=result, code='1', message='策略名称未改变')
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


# 直接执行策略
def executeStrategy(userId, strategy_id):
    # 查询策略基本配置
    strategy_base_info = DB.getStrategyDetail(creator=userId, strategy_id=strategy_id)

    # 执行poc
    print("strategy_poc: strategy_id ||", strategy_id)
    regression_result = strategyTool.strategy_poc(strategy_id, strategy_base_info.start_time,
                                                  strategy_base_info.end_time,
                                                  strategy_base_info.init_balance)

    # 记录插入 strategy_log  返回最新 strategy_log_id
    strategy_log_id = DB.insertStrategyLog(strategy_id=strategy_id, start_time=strategy_base_info.start_time,
                                           end_time=strategy_base_info.end_time,
                                           userId=userId, coin_category=strategy_base_info.coin_category,
                                           init_balance=strategy_base_info.init_balance)

    response = {
        "strategy_base_info": strategy_base_info.__dict__,
        "regression_result": regression_result.__dict__,
        "strategy_log_id": strategy_log_id
    }
    result = ResponseModel(data=response, code='1', message='success')
    return result


# mobile 执行策略
def mob_executeStrategy(userId, strategy_id, start_time, end_time, coin_category, init_balance):
    # 更新策略
    DB.mob_updateStrategy(userId=userId, strategy_id=strategy_id, start_time=start_time, end_time=end_time,
                          coin_category=coin_category, init_balance=init_balance)

    # 执行策略
    print("strategy_poc: strategy_id ||", strategy_id)
    result = strategyTool.strategy_poc(strategy_id=strategy_id, start_time=start_time, end_time=end_time,
                                       init_balance=init_balance)

    if result is False:
        print(result)
        response = ResponseModel(data=result, code='0', message='success')
        print(response)
        return response

    else:
        # 策略基本信息
        # 这里如果没有该策略？
        strategy_base_info = DB.getStrategyDetail(creator=userId, strategy_id=strategy_id)

        # 策略没有配置相应 买卖条件； buy_signal and sell_signal

        # 返回策略 trade_history 历史数据
        # strategy_trade_history = DB.mob_trade_history(strategy_log_id=strategy_log_id)
        result = result.__dict__
        data = {
            'regression_result': result,
            'strategy_base_info': strategy_base_info.__dict__,
            # 'strategy_log_id': strategy_log_id,
            # 'strategy_trade_history': strategy_trade_history.__dict__
        }

        print(result)
        response = ResponseModel(data=data, code='1', message='success')
        print(response)
        return response


        # 记录插入 strategy_log  返回最新 strategy_log_id
        # strategy_log_id = DB.insertStrategyLog(strategy_id=strategy_id, start_time=start_time, end_time=end_time,
        #                                        userId=userId, coin_category=coin_category, init_balance=init_balance)


# mobile 获取策略历史列表
def mob_strategy_trade_history(userId, strategy_id):
    trade_history_list = []

    trade_historys = DB.mob_trade_history(strategy_id=strategy_id, creator=userId)

    for trade_history in trade_historys:
        trade_history_list.append(trade_history.__dict__)

    response = ResponseModel(data=trade_history_list, code="1", message="success")

    return response
