from flask import Flask, request, session, make_response
import DB as db
import json
import os
import web.app.controller as controller
from strategy import main
from facilties.functional import JsonExtendEncoder, HttpResponseModel

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
    strategyLogList = controller.loadLogList(session['userId'])
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


@app.route('/saveStrategyConf', methods=['post'])
def saveStrategyConf():
    session.permanent = True
    session['userId'] = 1
    # strategyId,userId,initBalance,startDate,endDate,strategyConfItemlist
    strategy_name = request.json.get("strategy_name")
    # print(strategy_Id)
    startDate = request.json.get("startDate")

    print(startDate)
    # print(start_Date)
    endDate = request.json.get("endDate")
    print(endDate)
    # print(end_Date)
    initBalance = request.json.get("initBalance")
    # print(init_Balance)
    strategyConfItemlist = request.json.get("strategyConfItemlist")
    coin_category = request.json.get("kind")

    regression_result = controller.saveStrategyConf(strategy_name=strategy_name, userId=session['userId'],
                                                    initBalance=initBalance,
                                                    startDate=startDate,
                                                    endDate=endDate,
                                                    coin_category=coin_category,
                                                    strategyConfItemlist=strategyConfItemlist)
    # regression_result = main.strategy_poc(strategy_id=strategyId, user_id=session['userId'],
    #                                       coin_category=coin_category,
    #                                       start_time=startDate, end_time=endDate,
    #                                        init_balance=initBalance)

    print(regression_result)
    # print(regression_result.__dict__)

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
    print(strategy_list)
    result = json.dumps({"list": strategy_list}, ensure_ascii=False, cls=JsonExtendEncoder)
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


if __name__ == "__main__":
    app.run(debug=True)
