from flask import Flask, request, make_response
import DB as db
import json
from datetime import datetime
from datetime import date
import web.app.controller as controller
from  initData.InitData import StrategyList

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

@app.route('/getStrategyInstanceList')
def getStrategyInstanceList():
    strategy_list = []
    strategyList = controller.getStrategy()
    for item in strategyList:
        # 如果不使用对象属性 __dict__ 则会显示其 内存地址；
        strategy_list.append(item.__dict__)
        print(item.__dict__)
    #print(strategy_list)
    #result = {"list": strategy_list}
    result = json.dumps({"list": strategy_list}, cls=JsonExtendEncoder)
    return result


class JsonExtendEncoder(json.JSONEncoder):
    """
        This class provide an extension to json serialization for datetime/date.
    """

    def default(self, o):
        """
            provide a interface for datetime/date
        """
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)


if __name__ == "__main__":
    app.run(debug=True)
