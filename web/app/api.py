from flask import Flask, request, session, make_response
import DB as db
import json
import os
import web.app.controller as controller
from strategy import main
from facilties.functional import JsonExtendEncoder

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
    strategyId = request.json.get("strategyId")
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

    controller.saveStrategyConf(strategyId=strategyId, userId=session['userId'], initBalance=initBalance,
                                startDate=startDate,
                                endDate=endDate,
                               coin_category=coin_category , strategyConfItemlist=strategyConfItemlist)
    regression_result = main.strategy_poc(strategy_id=strategyId, user_id=session['userId'],
                                          coin_category=coin_category,
                                          start_time=startDate, end_time=endDate,
                                           init_balance=initBalance)
    print(regression_result)
    #print(regression_result.__dict__)

    response = make_response(
        json.dumps({'result': regression_result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


if __name__ == "__main__":
    app.run(debug=True)
