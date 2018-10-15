from util.ReadData import read_datas


class Position:
    def __init__(self, timestamp, start_time, end_time, balance):
        self.start_time = start_time
        self.end_time = end_time
        self.T = timestamp
        self.balance = balance
        self.init_balance = balance
        self.datas = read_datas(start_time, end_time).sort_values(by='id', axis=0, ascending=True)
        self.price = 0.00
        # 持币量
        self.coin_amount = 0.000000
        # 总币值
        self.coin_total = 0.00
        self.total = 0.00


        # 仓位
        self.coin_cash_rate = 0.0000


    # 数据库持久化
    def insert(self):
        return 0
