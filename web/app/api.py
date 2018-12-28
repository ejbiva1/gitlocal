from flask import Flask, request, session, make_response
import DB as db
import json
import os
import web.app.controller as controller
from strategy import main
from facilties.functional import JsonExtendEncoder, HttpResponseModel
from flask import Flask, Blueprint, render_template, request, redirect, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'


@app.route('/startStrategy', methods=['POST'])
def startStrategy():
    strategyId = request.json.get("strategyId")
    startTime = request.json.get("startTime")
    endTime = request.json.get("endTime")
    initBalance = request.json.get("initBalance")
    coinCategory = request.json.get("coinCategory")
    if 1000000 >= initBalance >= 10000:
        controller.startStartStrategy(strategyId, initBalance, startTime, endTime)
        return make_response(json.dumps({'result': 'strategy started'}))
    else:
        return make_response(json.dumps({'result': 'pls be sure initBalance is correct'}))


@app.route('/loadLogList', methods=['POST'])
def loadLogList():
    strategy_log_list = []
    session.permanent = True
    session['userId'] = 1

    strategy_id = request.json.get('strategy_id')
    if strategy_id is None:
        strategy_id = 0

    strategyLogList = controller.loadLogList(session['userId'], strategy_id)
    for item in strategyLogList:
        strategy_log_list.append(item.__dict__)
    result = json.dumps({"list": strategy_log_list}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/getLogDetail/<int:strategyLogId>', methods=['post'])
def getLogDetail(strategyLogId):
    session.permanent = True
    session['userId'] = 1
    log_details = controller.getLogDetail(strategyLogId, session['userId'])

    result = json.dumps({'list': log_details.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return result


# 保存并执行 策略
@app.route('/saveStrategyConf', methods=['post'])
def saveStrategyConf():
    session.permanent = True
    session['userId'] = 1

    strategy_name = request.json.get("strategy_name")
    strategy_id = request.json.get("strategy_id")
    start_time = request.json.get("start_time")
    end_time = request.json.get("end_time")
    init_balance = request.json.get("init_balance")
    strategyConfItemlist = request.json.get("strategyConfItemlist")
    coin_category = request.json.get("coin_category")
    strategy_oper = request.json.get('strategy_oper')

    regression_result = controller.saveStrategyAndRun(strategy_id=strategy_id,
                                                      strategy_name=strategy_name,
                                                      userId=session['userId'],
                                                      init_balance=init_balance,
                                                      start_time=start_time,
                                                      end_time=end_time,
                                                      coin_category=coin_category,
                                                      strategyConfItemlist=strategyConfItemlist,
                                                      strategy_oper=strategy_oper)

    response = make_response(
        json.dumps({'result': regression_result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/getALLStrategy', methods=['post'])
def getALLStrategy():
    strategy_list = []
    session.permanent = True
    session['userId'] = 1
    strategyList = controller.getALLStrategy(session['userId'])
    for item in strategyList:
        strategy_list.append(item.__dict__)
    result = json.dumps({"list": strategy_list}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/getStrategyDetail', methods=['post'])
def getStrategyDetail():
    strategy_id = request.json.get('strategy_id')
    session.permanent = True
    session['userId'] = 1
    strategy = controller.getStrategyDetail(creator=session['userId'], strategy_id=strategy_id)

    result = json.dumps({"result": strategy.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/checkStrategyName', methods=['post'])
def checkStrategyName():
    session.permanent = True
    session['userId'] = 1

    strategy_id = request.json.get("strategy_id")
    if strategy_id is None:
        strategy_id = 0
    strategy_name = request.json.get("strategy_name")
    is_strategy_name_exist = controller.checkStrategyName(strategy_name=strategy_name, creator=session['userId'],
                                                          strategy_id=strategy_id)

    result = json.dumps({"result": is_strategy_name_exist.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/saveStrategyName', methods=['post'])
def saveStrategyName():
    session.permanent = True
    session['userId'] = 1

    strategy_name = request.json.get("strategy_name")
    strategy_id = request.json.get("strategy_id")
    result = controller.saveStrategyName(strategy_name=strategy_name, strategy_id=strategy_id,
                                         creator=session['userId'])

    result = json.dumps({"result": result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/deleteStrategyLogById', methods=['post'])
def deleteStrategyLogById():
    strategy_log_id = request.json.get("strategy_log_id")

    try:
        result = controller.deleteStrategyLogById(strategy_log_id)

        result = json.dumps({"result": result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
        # response = HttpResponseModel(result)
        response = make_response(result);
        response.status = "200"
        response.headers["Content-Type"] = "application/json"

        return response

    except ZeroDivisionError as e:
        print('except:', e)


@app.route('/getStrategy', methods=['post'])
def getStrategy():
    strategy_id = request.json.get('strategy_id')
    session.permanent = True
    session['userId'] = 1

    try:

        strategy_confs = controller.getStrategy(creator=session['userId'], strategyId=strategy_id)

        result = json.dumps({"result": strategy_confs.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)

        response = make_response(result)
        response.status = "200"
        response.headers["Content-Type"] = "application/json"

        return response

    except ZeroDivisionError as e:
        print('except:', e)


# 暂存 或  新添加 策略
@app.route('/saveStrategyConfOrUpdate', methods=['post'])
def saveStrategy():
    session.permanent = True
    session['userId'] = 1
    strategy_id = request.json.get('strategy_id')
    print(strategy_id)
    if strategy_id is None:
        strategy_id = 0
    strategy_name = request.json.get("strategy_name")
    start_time = request.json.get("start_time")
    end_time = request.json.get("end_time")
    init_balance = request.json.get("init_balance")
    strategy_conf_item_list = request.json.get("strategyConfItemlist")
    coin_category = request.json.get("coin_category")
    strategy_oper = request.json.get("strategy_oper")

    result = controller.saveStrategyConfOrUpdate(
        strategy_id=strategy_id,
        strategy_name=strategy_name,
        userId=session['userId'],
        init_balance=init_balance,
        start_time=start_time,
        end_time=end_time,
        coin_category=coin_category,
        strategyConfItemlist=strategy_conf_item_list, strategy_oper=strategy_oper)
    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/executeStrategy', methods=['post'])
def executeStrategy():
    session.permant = True
    session['userId'] = 1
    strategy_id = request.json.get('strategy_id')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    coin_category = request.json.get('coin_category')
    init_balance = request.json.get('init_balance')

    result = controller.mob_executeStrategy(userId=session['userId'], strategy_id=strategy_id,
                                            start_time=start_time,
                                            end_time=end_time, init_balance=init_balance,
                                            coin_category=coin_category)

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


# 诗丽 手机端 调用 该接口， 执行poc 并返回相应历史数据；
@app.route('/mob_executeStrategy', methods=['post'])
def mob_executeStrategy():
    session.permant = True
    session['userId'] = 1
    strategy_id = request.json.get('strategy_id')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    init_balance = request.json.get('init_balance')
    coin_category = request.json.get('coin_category')

    result = controller.mob_executeStrategy(userId=session['userId'], strategy_id=strategy_id, start_time=start_time,
                                            end_time=end_time, init_balance=init_balance, coin_category=coin_category)

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


# 诗丽 手机端 调用 该接口， 获取策略 回测历史数据
@app.route('/mob_strategytradehistory', methods=['post'])
def mob_strategytradehistory():
    session.permant = True
    session['userId'] = 1

    strategy_id = request.json.get('strategy_id')

    result = controller.mob_strategy_trade_history(userId=session['userId'], strategy_id=strategy_id)

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


# 诗丽 手机端 调用 该接口， 获取我的策略列表 策略名称 最后一次调用时间 总的调用次数
@app.route('/mob_getMyStrategyList', methods=['post'])
def mob_get_my_strategy_list():
    session.permant = True
    session['userId'] = 1
    result = controller.mob_my_strategy_list(userId=session['userId'])

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


# 诗丽 手机端 调用 该接口， 获取某个策略回测列表 每次执行的结果 （策略名称，回测时间，策略收益率，基准收益率，最大回撤）
@app.route('/mob_getStrategyLogList', methods=['post'])
def mob_get_strategy_log_list():
    session.permant = True
    session['userId'] = 1
    strategy_id = request.json.get('strategy_id')
    result = controller.mob_get_strategy_log_list(strategy_id=strategy_id, user_id=session['userId'])

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


# 诗丽 手机端 调用 该接口， 获取回测图标数据
@app.route('/mob_getDataArrays', methods=['post'])
def mob_get_data_array():
    # session.permant = True
    # session['userId'] = 1
    strategy_log_id = request.json.get('strategy_log_id')
    result = controller.mob_get_strategy_account_list(strategy_log_id=strategy_log_id)

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


if __name__ == "__main__":
    app.run(debug=True)
