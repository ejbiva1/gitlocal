import pandas as pd
from util.ReadData import read_datas
import decimal
from util.Trader import *


class SellB:
    # 初始化策略参数
    def __init__(self, start_time, end_time, balance):
        self.start_time = start_time
        self.end_time = end_time
        # self.T = timestamp
        self.balance = balance
        self.init_balance = balance
        # self.pre_T = timestamp - 3600
        # self.next_T = timestamp + 3600

        # self.summary = rep.Summary()
        # self.position = pos.Position(balance)
        self.datas = read_datas(start_time, end_time).sort_values(by='id', axis=0, ascending=True)

    # # 获取[ T + (-)1 ]时间区间的数据
    # def filter(self):
    #     df = self.datas
    #     df = df[(df['id'] >= self.pre_T)]
    #     df = df[(df['id'] <= self.next_T)]
    #     return df

    def condition_1(self, T):
        df = self.datas[(self.datas['id'] == T)]
        df = df[(df['close'] > df['open'])]
        if df.empty:
            return False
        else:
            return True

    def condition_2(self, T):
        pre_T = T - 3600
        df1 = self.datas[(self.datas['id'] == T)]
        df2 = self.datas[(self.datas['id'] == pre_T)]
        # vol is at row[6] (from 0-7 ,begin with id not kline_id)
        try:
            if df1.iat[0, 6] > df2.iat[0, 6]:
                # print(df1.iat[0, 6])
                # print(df2.iat[0, 6])
                return True
            else:
                return False
        except IndexError:
            return False

    def condition_3(self, T):
        pre_T = T - 3600
        df1 = self.datas[(self.datas['id'] == T)]
        df2 = self.datas[(self.datas['id'] == pre_T)]
        # close is at row[2] (from 0-7 ,begin with id not kline_id)
        try:
            if df1.iat[0, 2] > df2.iat[0, 1]:
                return True
            else:
                return False
        except IndexError:
            return False

    def condition_4(self, T):
        pre_T = T - 3600
        df1 = self.datas[(self.datas['id'] == T)]
        df2 = self.datas[(self.datas['id'] == pre_T)]
        # high is at row[4] (from 0-7 ,begin with id not kline_id)
        try:
            if df1.iat[0, 4] > df2.iat[0, 4]:
                return True
            else:
                return False
        except IndexError:
            return False

    def condition_a(self, T):
        next_T = T + 3600
        df1 = self.datas[(self.datas['id'] == T)]
        df2 = self.datas[(self.datas['id'] == next_T)]
        # high is at row[4] (from 0-7 ,begin with id not kline_id)
        if df2.iat[0, 4] >= decimal.Decimal(df1.iat[0, 2]) * decimal.Decimal('1.02'):
            return True
        else:
            return False

    def condition_b(self, T):
        pre_T = T - 3600
        next_T = T + 3600
        df1 = self.datas[(self.datas['id'] == pre_T)]
        df2 = self.datas[(self.datas['id'] == next_T)]
        diff = decimal.Decimal(df1.iat[0, 1] - df1.iat[0, 2]) * decimal.Decimal('0.1')
        # HIGH(T+1)>=OPEN(T-1) - [OPEN(T-1)-CLOSE(T-1)]10%
        if df2.iat[0, 4] >= (decimal.Decimal(df1.iat[0, 1]) - diff):
            return True
        else:
            return False

    def condition_c(self, T):
        # todo LOW(T+1)< 买入价格95%，则决策卖出，卖出价格为买入价格95%，卖出仓位=T日买入仓位
        # df1 = self.datas[(self.datas['id'] == self.pre_T)]
        # df2 = self.datas[(self.datas['id'] == self.next_T)]
        # diff = decimal.Decimal(df1.iat[0, 1] - df1.iat[0, 2]) * decimal.Decimal('0.1')
        # if df2.iat[0, 4] >= (decimal.Decimal(df1.iat[0, 1]) - diff):
        return True

    def strategy(self, T):
        if (self.condition_1(T) and self.condition_2(T)
                and self.condition_3(T) and self.condition_4(T)):

            if self.condition_a(T):
                # todo 卖出仓位=T日买入仓位，卖出价格为CLOSE(T)1.02
                return True
            else:
                if self.condition_b(T):
                    # todo 则卖出价格为OPEN(T-1) - [OPEN(T-1)-CLOSE(T-1)]10%。卖出仓位=T日买入仓位
                    return True
                else:
                    if self.condition_c(T):
                        # todo 卖出价格为买入价格95%，卖出仓位=T日买入仓位
                        return True
                    else:
                        # todo 卖出价格为CLOSE(T+1)，卖出仓位=T日买入仓位
                        return True
        else:
            # todo 卖出价格为CLOSE(T+1)，卖出仓位=T日买入仓位
            return True

    def run_strategy(self):
        df = self.datas
        for timestamp in df['id']:
            return self.strategy(timestamp)
        # 卖出结算
        Trader.sell()


if __name__ == '__main__':
    sellB = SellB(1508990400, 1509001200, 200)
    # sellB = SellB(1508997600, 1508990400, 1511481600, 200)
    # print(sellB.filter())
    # print(sellB.condition_filter())
    # print(sellB.test())
    # print(sellB.condition_1())
    # print(sellB.condition_b(1508994000))
    print(sellB.run_strategy())
