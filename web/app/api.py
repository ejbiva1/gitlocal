from flask import Flask, request, session, make_response
import DB as db
import json
import os
import web.app.controller as controller
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


if __name__ == "__main__":
    app.run(debug=True)
