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
    if initBalance <= 1000000 and initBalance >= 10000:
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
    print(strategy_log_list)
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

    print(regression_result)

    response = make_response(json.dumps({'result': regression_result}, ensure_ascii=False, cls=JsonExtendEncoder))
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
    print(strategy_list)
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

    strategy_name = request.json.get("strategy_name")
    is_strategy_name_exist = controller.checkStrategyName(strategy_name, session['userId'])

    print(is_strategy_name_exist.__dict__)
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

    print(result.__dict__)
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
        print(result)
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

        response = make_response(result);
        response.status = "200"
        response.headers["Content-Type"] = "application/json"

        return response

    except ZeroDivisionError as e:
        print('except:', e)


@app.route('/saveStrategy', methods=['post'])
def saveStrategy():
    session.permanent = True
    session['userId'] = 1
    strategy_id = request.json.get('strategy_id')
    print(strategy_id)
    if strategy_id is None:
        strategy_id = 0;
    strategy_name = request.json.get("strategy_name")
    start_time = request.json.get("start_time")
    end_time = request.json.get("end_time")
    init_balance = request.json.get("init_balance")
    strategyConfItemlist = request.json.get("strategyConfItemlist")
    coin_category = request.json.get("coin_category")

    result = controller.saveStrategy(
        strategy_id=strategy_id,
        strategy_name=strategy_name,
        userId=session['userId'],
        init_balance=init_balance,
        start_time=start_time,
        end_time=end_time,
        coin_category=coin_category,
        strategyConfItemlist=strategyConfItemlist)

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/updateStrategy', methods=['post'])
def updateStrategy():
    session.permanent = True
    session['userId'] = 1
    strategy_id = request.json.get('strategy_id')
    print(strategy_id)
    if strategy_id is None:
        strategy_id = 0;
    strategy_name = request.json.get("strategy_name")
    start_time = request.json.get("start_time")
    end_time = request.json.get("end_time")
    init_balance = request.json.get("init_balance")
    coin_category = request.json.get("coin_category")

    result = controller.updateStrategy(
        strategy_id=strategy_id,
        strategy_name=strategy_name,
        userId=session['userId'],
        init_balance=init_balance,
        start_time=start_time,
        end_time=end_time,
        coin_category=coin_category
    )

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

    result = controller.executeStrategy(userId=session['userId'], strategy_id=strategy_id)

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/mob_executeStrategy', methods=['post'])
def mob_executeStrategy():
    session.permant = True
    session['userId'] = 1
    strategy_id = request.json.get('strategy_id')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    print(end_time)
    init_balance = request.json.get('init_balance')
    coin_category = request.json.get('coin_category')

    result = controller.mob_executeStrategy(userId=session['userId'], strategy_id=strategy_id, start_time=start_time,
                                            end_time=end_time, init_balance=init_balance, coin_category=coin_category)

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


if __name__ == "__main__":
    app.run(debug=True)
