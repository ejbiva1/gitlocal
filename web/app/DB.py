import pymysql
connection = pymysql.connect("localhost", "root", "root", "quant_coin", charset='utf8')
def getStrategyInstanceList():
   cursor = connection.cursor()
   strategyInstanceList = []
   # SQL 查询语句
   sql = "SELECT strategy_instance_id,strategy_instance_description,start_date,end_date,init_balance,create_time,strategy_id,margin_return FROM strategy_instance;"

   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      # 打印结果
      pro = StrategyInstance(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
      strategyInstanceList.append(pro)
   cursor.close()
   return strategyInstanceList
def getStrategyInstanceLogList():
   cursor = connection.cursor()
   strategyInstanceList = []
   # SQL 查询语句
   sql = "SELECT strategy_instance_log_id,strategy_instance_id,transaction_direction,coin_category,create_time FROM strategy_instance_log where strategy_instance_id=%s"

   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      # 打印结果
      pro = StrategyInstanceLog(row[0], row[1], row[2], row[3], row[4])
      #print("row[0]:"+str(row[0])+"|row[1]:"+row[1]+"|row[2]:"+str(row[2])+"|row[3]:"+str(row[3])+"|row[4]:"+row[4]+"|row[5]:"+str(row[5])+"|row[6]:"+row[6]+"|row[7]:"+str(row[7]))
      strategyInstanceList.append(pro)
   cursor.close()
   return strategyInstanceList
def checkUser():
    cursor = connection.cursor()
    strategyInstanceList = []
    # SQL 查询语句
    sql = "SELECT strategy_instance_log_id,strategy_instance_id,transaction_direction,coin_category,create_time FROM strategy_instance_log where strategy_instance_id=%s"

    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        # 打印结果
        pro = StrategyInstanceLog(row[0], row[1], row[2], row[3], row[4])
        # print("row[0]:"+str(row[0])+"|row[1]:"+row[1]+"|row[2]:"+str(row[2])+"|row[3]:"+str(row[3])+"|row[4]:"+row[4]+"|row[5]:"+str(row[5])+"|row[6]:"+row[6]+"|row[7]:"+str(row[7]))
        strategyInstanceList.append(pro)
    cursor.close()
    return strategyInstanceList
class StrategyInstance:
    strategyInstanceId = 0
    strategyInstanceDescription = ""
    startDate = ""
    endDate = ""
    initBalance = 0
    createTime = ""
    strategyId = 0
    marginReturn = 0
    def __init__(self, strategyInstanceId ,strategyInstanceDescription,startDate,endDate,initBalance,createTime,strategyId,marginReturn):
        self.strategyInstanceId = strategyInstanceId
        self.strategyInstanceDescription = strategyInstanceDescription
        self.startDate = startDate
        self.endDate = endDate
        self.initBalance = initBalance
        self.createTime = createTime
        self.strategyId = strategyId
        self.marginReturn = marginReturn
    def getStrategyInstanceId(self):
        return self.strategyInstanceId
    def getStrategyInstanceDescription(self):
        return self.strategyInstanceDescription
    def getStartDate(self):
        return self.startDate
    def getEndDate(self):
        return self.endDate
    def getInitBalance(self):
        return self.initBalance
    def getCreateTime(self):
        return self.createTime
    def getStrategyId(self):
        return self.strategyId
    def getMarginReturn(self):
        return self.marginReturn

    def setStrategyInstanceId(self,strategyInstanceId):
        self.strategyInstanceId = strategyInstanceId

    def setStrategyInstanceDescription(self,strategyInstanceDescription):
        self.strategyInstanceDescription = strategyInstanceDescription

    def setStartDate(self,startDate):
        self.startDate = startDate

    def setEndDate(self,endDate):
        self.endDate = endDate

    def setInitBalance(self,initBalance):
        self.initBalance = initBalance

    def setCreateTime(self,createTime):
        self.createTime = createTime

    def setStrategyId(self,strategyId):
        self.strategyId = strategyId

    def setMarginReturn(self,marginReturn):
        self.marginReturn

class Strategy:
    strategy_id = 0
    strategy_name = ""
    description = ""
    create_time = ""
    update_time = ""
    loading_times = 0
    creator = 0
    script_url = ""
    peroid = 0
    def __init__(self,strategy_id,strategy_name,description,create_time,update_time,loading_times,creator,script_url,peroid):

    def get_strategy_id(self):
        return self.strategy_id
    def get_strategy_name(self):
        return self.strategy_name
    def get_description(self):
        return self.description
    def get_create_time(self):
        return self.create_time
    def get_update_time(self):
        return self.update_time
    def get_loading_times(self):
        return self.loading_times
    def get_creator(self):
        return self.creator
    def get_script_url(self):
        return self.script_url
    def get_peroid(self):
        return self.peroid

    def set_strategy_id(self,strategy_id):
        self.strategy_id = strategy_id
    def set_strategy_name(self,strategy_name):
        self.strategy_name = strategy_name
    def set_description(self,description):
        self.description = description
    def set_create_time(self,create_time):
        self.create_time = create_time
    def set_update_time(self,update_time):
        self.update_time = update_time
    def set_loading_times(self,loading_times):
        self.loading_times = loading_times
    def set_creator(self,creator):
        self.creator = creator
    def set_script_url(self,script_url):
        self.script_url = script_url
    def set_peroid(self,peroid):
        self.peroid = peroid
#getStrategyInstanceList()