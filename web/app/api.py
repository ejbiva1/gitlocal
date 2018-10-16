from flask import Flask,request,make_response
import DB as db
import json
app = Flask(__name__)

@app.route('/startStrategy',methods=['POST'])
def startStrategy():

    strategyId = request.form.get("strategyId")
    startTime = request.args.get("startTime")
    startTime = request.json.get("startTime")
    endTime = request.json.get("endTime")
    initBalance = request.json.get("initBalance")
    coinCategory = request.json.get("coinCategory")
    print("strategyId:"+strategyId)
    strategyInstanceList = db.getStrategyInstanceList()
    htmlStr = "<button>Save</button>"
    result = {"list":strategyInstanceList}
    htmlStr = json.dumps(result)
    return htmlStr

@app.route('/loadLogList',methods=['POST'])
def loadLogList():
    strategyInstanceList = db.getStrategyInstanceList()
    htmlStr = "<button>Save</button>"
    result = {"list":strategyInstanceList}
    htmlStr = json.dumps(result)
    return htmlStr
if __name__ == "__main__":
    app.run(debug=True)
