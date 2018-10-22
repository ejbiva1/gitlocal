import pymysql
connection = pymysql.connect("localhost", "root", "root", "quant_coin", charset='utf8')

class StrategyLog:
    strategy_log_id = 0
    strategy_id = 0
    start_date = ""
    end_date = ""
    init_balance = 0.0
    coin_category = 0
    creator = 0
    create_time = ""
    execution_result = ""
    def __init__(self, strategy_log_id,
    strategy_id,
    start_date,
    end_date,
    init_balance,
    coin_category,
    creator,
    create_time,
    execution_result):
        self.strategy_log_id = strategy_log_id
        self.strategy_id = strategy_id
        self.start_date = start_date
        self.end_date = end_date
        self.init_balance = init_balance
        self.coin_category = coin_category
        self.creator = creator
        self.create_time = create_time
        self.execution_result = execution_result
    def get_strategy_log_id(self):
        return self.strategy_log_id
    def get_strategy_id(self):
        return self.strategy_id
    def get_start_date(self):
        return self.start_date
    def get_end_date(self):
        return self.end_date
    def get_init_balance(self):
        return self.init_balance
    def get_coin_category(self):
        return self.coin_category
    def get_creator(self):
        return self.creator
    def get_create_time(self):
        return self.create_time
    def get_execution_result(self):
        return self.execution_result

    def set_strategy_log_id(self,strategy_log_id):
        self.strategy_log_id = strategy_log_id

    def set_strategy_id(self,strategy_id):
        self.strategy_id = strategy_id

    def set_start_date(self,start_date):
        self.start_date = start_date

    def set_end_date(self,end_date):
        self.end_date = end_date

    def set_init_balance(self,init_balance):
        self.init_balance = init_balance

    def set_coin_category(self,coin_category):
        self.coin_category = coin_category

    def set_creator(self,creator):
        self.creator = creator

    def set_create_time(self,create_time):
        self.create_time = create_time
    def set_execution_result(self,execution_result):
        self.execution_result = execution_result


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
        self.strategy_id = strategy_id
        self.strategy_name = strategy_name
        self.description = description
        self.create_time = create_time
        self.update_time = update_time
        self.loading_times = loading_times
        self.creator = creator
        self.script_url = script_url
        self.peroid = peroid
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


class StrategyAccount:
    strategy_account_id = 0
    strategy_log_id = 0
    current_cash_balance = 0.0
    current_coin_balance = 0.0
    cost  = 0.0
    total_net_balance  = 0.0
    current_net_value  = 0.0
    current_total_margin_rate = 0.0
    current_margin_rate = 0.0
    current_position = 0.0
    signal = 0
    transaction_status = 0
    t = "'"
    open = 0.0
    close  = 0.0
    high = 0.0
    low  = 0.0
    def __init__(self,strategy_account_id,
    strategy_log_id,
    current_cash_balance,
    current_coin_balance,
    cost,
    total_net_balance,
    current_net_value,
    current_total_margin_rate,
    current_margin_rate,
    current_position,
    signal,
    transaction_status,
    t,
    open,
    close,
    high,
    low):
        self.strategy_account_id = strategy_account_id
        self.strategy_log_id = strategy_log_id
        self.current_cash_balance = current_cash_balance
        self.current_coin_balance = current_coin_balance
        self.cost = cost
        self.total_net_balance = total_net_balance
        self.current_net_value = current_net_value
        self.current_total_margin_rate = current_total_margin_rate
        self.current_margin_rate = current_margin_rate
        self.current_position = current_position
        self.signal = signal
        self.transaction_status = transaction_status
        self.t = t
        self.open = open
        self.close = close
        self.high = high
        self.low = low
    def get_strategy_account_id(self):
        return self.strategy_account_id
    def get_strategy_log_id(self):
        return self.strategy_log_id
    def get_current_cash_balance(self):
        return self.current_cash_balance
    def get_current_coin_balance(self):
        return self.current_coin_balance
    def get_cost(self):
        return self.cost
    def get_total_net_balance(self):
        return self.total_net_balance
    def get_current_net_value(self):
        return self.current_net_value
    def get_current_total_margin_rate(self):
        return self.current_total_margin_rate

    def get_current_margin_rate(self):
        return self.current_margin_rate
    def get_current_position(self):
        return self.current_position
    def get_signal(self):
        return self.signal
    def get_transaction_status(self):
        return self.transaction_status
    def get_t(self):
        return self.t
    def get_open(self):
        return self.open
    def get_close(self):
        return self.close
    def get_high(self):
        return self.high
    def get_low(self):
        return self.low


class StrategyTransaction:
    strategy_transaction_id = 0
    strategy_account_id = 0
    t = ""
    cost = 0.0
    volumn = 0.0
    commission = 0.0
    pre_position = 0.0
    post_position = 0.0
    position_gap = 0.0
    pre_balance = 0.0
    post_balance = 0.0
    balance_gap = 0.0
    def __init__(self,strategy_account_id,
    strategy_log_id,
    current_cash_balance,
    current_coin_balance,
    cost,
    total_net_balance,
    current_net_value,
    current_total_margin_rate,
    current_margin_rate,
    current_position,
    signal,
    transaction_status,
    t,
    open,
    close,
    high,
    low):
        self.strategy_account_id = strategy_account_id
        self.strategy_log_id = strategy_log_id
        self.current_cash_balance = strategy_log_id
        self.current_coin_balance = current_coin_balance
        self.cost = cost
        self.total_net_balance = total_net_balance
        self.current_net_value = current_net_value
        self.current_total_margin_rate = current_total_margin_rate
        self.current_margin_rate = current_margin_rate
        self.current_position = current_position
        self.signal = signal
        self.transaction_status = transaction_status
        self.t = t
        self.open = open
        self.close = close
        self.high = high
        self.low = low

    def get_strategy_account_id(self):
        return self.strategy_account_id
    def get_strategy_log_id(self):
        return self.strategy_log_id
    def get_current_cash_balance(self):
        return self.current_cash_balance
    def get_current_coin_balance(self):
        return self.current_coin_balance
    def get_cost(self):
        return self.cost
    def get_total_net_balance(self):
        return self.total_net_balance
    def get_current_net_value(self):
        return self.current_net_value
    def get_current_total_margin_rate(self):
        return self.current_total_margin_rate
    def get_current_margin_rate(self):
        return self.current_margin_rate
    def get_current_position(self):
        return self.current_position
    def get_signal(self):
        return self.signal
    def get_transaction_status(self):
        return self.transaction_status
    def get_t(self):
        return self.t
    def get_open(self):
        return self.open
    def get_close(self):
        return self.close
    def get_high(self):
        return self.high
    def get_low(self):
        return self.low

    def set_strategy_account_id(self,strategy_account_id):
        self.strategy_account_id = strategy_account_id
    def set_strategy_log_id(self,strategy_log_id):
        self.strategy_log_id = strategy_log_id
    def set_current_cash_balance(self,current_cash_balance):
        self.current_cash_balance = current_cash_balance
    def set_current_coin_balance(self,current_coin_balance):
        self.current_coin_balance = current_coin_balance
    def set_cost(self,cost):
        self.cost = cost
    def set_total_net_balance(self,total_net_balance):
        self.total_net_balance = total_net_balance
    def set_current_net_value(self,current_net_value):
        self.current_net_value = current_net_value
    def set_current_total_margin_rate(self,current_total_margin_rate):
        self.current_total_margin_rate = current_total_margin_rate
    def set_current_margin_rate(self,current_margin_rate):
        self.current_margin_rate = current_margin_rate
    def set_current_position(self,current_position):
        self.current_position = current_position
    def set_signal(self,signal):
        self.signal = signal
    def set_transaction_status(self,transaction_status):
        self.transaction_status = transaction_status
    def set_t(self,t):
        self.t = t
    def set_open(self,open):
        self.open = open
    def set_close(self,close):
        self.close = close
    def set_high(self,high):
        self.high = high
    def set_low(self,low):
        self.low = low


def getStrategy():
    cursor = connection.cursor()
    strategyList = []
    # SQL 查询语句
    sql = "SELECT strategy_id,"\
    " strategy_name,"\
    " description,"\
    " create_time,"\
    " update_time,"\
    " loading_times,"\
    " creator,"\
    " script_url,"\
    " peroid "\
    " FROM strategy"

    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        # 打印结果
        strategy = Strategy(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[7])
        strategyList.append(strategy)
    cursor.close()
    return strategyList


def getStrategyLogList(creator):
   cursor = connection.cursor()
   strategyLogList = []
   # SQL 查询语句
   sql = " SELECT strategy_log_id,"\
         " strategy_id,"\
         " start_date," \
         " end_date," \
         " init_balance," \
         " coin_category," \
         " creator," \
         " create_time," \
         " execution_result" \
         " FROM strategy_log" \
         " where creator=%s"

   # 执行SQL语句
   cursor.execute(sql,creator)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      # 打印结果
      pro = StrategyLog(row[0], row[1], row[2], row[3], row[4],row[5], row[6], row[7], row[8])
      #print("row[0]:"+str(row[0])+"|row[1]:"+row[1]+"|row[2]:"+str(row[2])+"|row[3]:"+str(row[3])+"|row[4]:"+row[4]+"|row[5]:"+str(row[5])+"|row[6]:"+row[6]+"|row[7]:"+str(row[7]))
      strategyLogList.append(pro)
   cursor.close()
   return strategyLogList


def getLogDetail(strategyLogId, creator):
    cursor = connection.cursor()
    log_details = []
    #   SQL 查询语句
    sql = " SELECT strategy_log_id,"\
         " strategy_id,"\
         " start_date," \
         " end_date," \
         " init_balance," \
         " coin_category," \
         " creator," \
         " create_time," \
         " execution_result" \
         " FROM strategy_log" \
         " where strategy_log_id=%s and creator=%s" %(strategyLogId, creator)

    # 执行SQL 语句
    cursor.execute(sql)

    results = cursor.fetchall()
    for row in results:
        pro = StrategyLog(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

        log_details.append(pro)
    cursor.close()
    return log_details

def getStrategyAccountList(strategyLogId):
   cursor = connection.cursor()
   strategyAccountList = []
   # SQL 查询语句
   sql = " SELECT strategy_account_id,strategy_log_id,current_cash_balance,current_coin_balance,cost,total_net_balance,current_net_value,"\
   " current_total_margin_rate,current_margin_rate,current_position,`signal`,transaction_status,t,open,close,high,low FROM strategy_account where strategy_log_id = %s"

   # 执行SQL语句
   cursor.execute(sql,strategyLogId)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      # 打印结果
      pro = StrategyAccount(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16])
      strategyAccountList.append(pro)
   cursor.close()
   return strategyAccountList

# list = getStrategyLogList(1)
# for sl in list:
#     print(sl.get_strategy_log_id())
#     print(sl.get_strategy_id())
#     print(sl.get_start_date())
#     print(sl.get_end_date())
#     print(sl.get_init_balance())
#     print(sl.get_coin_category())
#     print(sl.get_creator())
#     print(sl.get_create_time())
#     print(sl.get_strategy_log_id())
#     print(sl.get_execution_result())
#
#
# list = getStrategyAccountList(1)
# for sl in list:
#     print("----------------------")
#     print(sl.get_strategy_account_id())
#     print(sl.get_strategy_log_id())
#     print(sl.get_current_cash_balance())
#     print(sl.get_current_coin_balance())
#     print(sl.get_cost())
#     print(sl.get_total_net_balance())
#     print(sl.get_current_net_value())
#     print(sl.get_current_total_margin_rate())
#     print(sl.get_current_margin_rate())
#     print(sl.get_current_position())
#     print(sl.get_signal())
#     print(sl.get_transaction_status())
#     print(sl.get_t())
#     print(sl.get_close())
#     print(sl.get_high())
#     print(sl.get_low())
