from flask import Flask, request, session
import DB as db
import json
import os
import web.app.controller as controller
from decimal import Decimal
from numbers import Number
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
        controller.startStartStrategy(strategyId,initBalance,startTime,endTime)
        return json.dumps({'result': 'strategy started'})
    else:
        return json.dumps({'result': 'pls be sure initBalance is correct'})


@app.route('/loadLogList', methods=['POST'])
def loadLogList():
    # 后端写死一个 session 对象，保存一个session['userId']
    session.permanent = True
    session['userId'] = 1
    strategy_log_list = []
    strategyLogList = controller.loadLogList(session['userId'])
    for item in strategyLogList:
        strategy_log_list.append(item.__dict__)
    print(strategy_log_list)
    result = json.dumps({"list": strategy_log_list}, ensure_ascii=False, cls=JsonExtendEncoder)
    return result


@app.route('/getLogDetail/<int:stratgyLogId>', methods=['post'])
def getLogDetail(stratgyLogId):
    log_details = []
    log_details_list = controller.getLogDetail(stratgyLogId, session['userId'])
    for item in log_details_list:
        print(item.__dict__)
        log_details.append(item.__dict__)
    result = json.dumps({'list': log_details}, ensure_ascii=False, cls=JsonExtendEncoder)

    return result


@app.route('/getStrategyInstanceList', methods=['post', 'put'])
def getStrategyInstanceList():
    strategy_list = []
    strategyList = controller.getStrategy()
    for item in strategyList:
        # print(item.__dict__)
        strategy_list.append(item.__dict__)

    # json.dumps 序列化时对中文默认使用的ascii编码 : json.dumps 序列化对象时 对中文默认使用 ascii编码
    result = json.dumps({"list": strategy_list}, cls=JsonExtendEncoder, ensure_ascii=False)
    return result


# 给URL 添加变量部分: 规则可以用 <converter:variable_name> 指定一个可选的转换器
@app.route('/getStrategyInstance/<int:strategy_id>', methods=['post', 'put'])
def getStrategyInstance(strategy_id):
    if request.method == 'post':
        strategyInstance = db.getStrategyInstance(strategy_id)
        # strategyInstance_list = []
        # strategyInstance_list.append(strategyInstance.__dict__)
        # result = json.dumps({'result': strategyInstance_list}, ensure_ascii=False, cls=JsonExtendEncoder)

        # python 对象 转化成 json 字符串
        result = json.dumps({'result': strategyInstance.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
        return result


if __name__ == "__main__":
    app.run(debug=True)
