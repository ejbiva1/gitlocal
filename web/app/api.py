from flask import Flask, request, make_response, session
import DB as db
import json
import web.app.controller as controller
from facilties.functional import JsonExtendEncoder

app = Flask(__name__)


@app.route('/startStrategy', methods=['POST'])
def startStrategy():
    strategyId = request.form.get("strategyId")
    startTime = request.args.get("startTime")
    startTime = request.json.get("startTime")
    endTime = request.json.get("endTime")
    initBalance = request.json.get("initBalance")
    coinCategory = request.json.get("coinCategory")
    print("strategyId:" + strategyId)
    strategyInstanceList = db.getStrategyInstanceList()
    htmlStr = "<button>Save</button>"
    result = {"list": strategyInstanceList}
    htmlStr = json.dumps(result)
    return htmlStr


@app.route('/loadLogList', methods=['POST'])
def loadLogList():
    strategyInstanceList = db.getStrategyInstanceList()
    htmlStr = "<button>Save</button>"
    result = {"list": strategyInstanceList}
    htmlStr = json.dumps(result)
    return htmlStr


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

#给URL 添加变量部分: 规则可以用 <converter:variable_name> 指定一个可选的转换器
@app.route('/getStrategyInstance/<int:strategy_id>', methods=['post', 'put'])
def getStrategyInstance(strategy_id):
    strategyInstance = db.getStrategyInstance(strategy_id)
    # strategyInstance_list = []
    # strategyInstance_list.append(strategyInstance.__dict__)
    # result = json.dumps({'result': strategyInstance_list}, ensure_ascii=False, cls=JsonExtendEncoder)

    # python 对象 转化成 json 字符串
    result = json.dumps({'result': strategyInstance.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
    return result


if __name__ == "__main__":
    app.run(debug=True)
