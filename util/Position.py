from util.ReadData import read_datas


class Position:
    def __init__(self, timestamp, start_date, end_date, balance):
        self.start_date = start_date
        self.end_date = end_date
        self.T = timestamp
        self.balance = balance
        self.init_balance = balance
        self.datas = read_datas(start_date, end_date).sort_values(by='id', axis=0, ascending=True)
        self.price = 0.00
        # 持币量
        self.coin_amount = 0.000000
        # 总币值
        self.total_net_balance = 0.00
        self.total = 0.00

        # 仓位
        self.coin_cash_rate = 0.0000


    # todo 数据库持久化
    def insert(self):
        return 0
