from util.ReadData import *
from decimal import Decimal


class Position:
    # todo 暂时使用strategy_id来确定到底读取什么维度的数据库
    def __init__(self, start_date, end_date, balance, strategy_type):
        self.start_date = start_date
        self.end_date = end_date
        # self.T = timestamp
        self.balance = balance
        self.init_balance = balance
        if strategy_type == 1 or strategy_type == 2:
            # todo 判断开始日期-12T是否存在
            self.datas = read_datas_1day(start_date, end_date).sort_values(by='id', axis=0, ascending=True)
        else:
            # self.datas = read_datas_60min(start_date, end_date).sort_values(by='id', axis=0, ascending=True)
            self.datas = read_datas_60min_test(start_date, end_date).sort_values(by='id', axis=0, ascending=True)
        self.price = Decimal(0.00)
        # 持币量
        self.coin_amount = Decimal('0.000000')
        # 总币值
        self.total_net_balance = Decimal(0.00)
        # 总资产
        self.total = Decimal(balance)

        # 仓位
        self.current_position = Decimal(0.0000)

    # todo 数据库持久化
    def insert(self):
        return 0


