from util.ReadData import read_datas_60min
from decimal import Decimal
from util.Trader import *


class BuyB:
    # 初始化策略参数
    def __init__(self, start_time, end_time, position):
        self.start_time = start_time
        self.end_time = end_time
        # self.balance = balance
        # self.init_balance = balance
        self.datas = position.datas
        self.idt = self.datas['id']
        self.position = position

    def condition_1(self, T):
        timestamp = T - 7200
        df = self.datas[(self.idt == timestamp)]
        df = df[(df['close'] > df['open'])]
        if df.empty:
            return False
        else:
            return True

    def condition_2(self, T):
        pre_T = T - 3600
        df = self.datas[(self.idt == pre_T)]
        try:
            if df.iat[0, 2] < df.iat[0, 1]:
                return True
            else:
                return False
        except IndexError:
            return False

    def condition_3(self, T):
        pre_T = T - 3600
        pre_2T = T - 7200
        df1 = self.datas[(self.idt == pre_T)]
        df2 = self.datas[(self.idt == pre_2T)]
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
        pre_2T = T - 7200
        df1 = self.datas[(self.idt == pre_T)]
        df2 = self.datas[(self.idt == pre_2T)]
        try:
            if df1.iat[0, 1] < df2.iat[0, 2]:
                return True
            else:
                return False
        except IndexError:
            return False

    def condition_5(self, T):
        pre_T = T - 3600
        pre_2T = T - 7200
        df1 = self.datas[(self.idt == pre_T)]
        df2 = self.datas[(self.idt == pre_2T)]
        # high is at row[4] (from 0-7 ,begin with id not kline_id)
        t2 = df2.iat[0, 4] - df2.iat[0, 3]
        t1 = df1.iat[0, 4] - df1.iat[0, 3]
        if t2 > t1:
            return True
        else:
            return False

    def condition_6(self, T):
        pre_T = T - 3600
        pre_2T = T - 7200
        df1 = self.datas[(self.idt == pre_T)]
        df2 = self.datas[(self.idt == pre_2T)]
        vol2 = Decimal(df2.iat[0, 6]) * Decimal('0.75')
        # HIGH(T+1)>=OPEN(T-1) - [OPEN(T-1)-CLOSE(T-1)]10%
        if df1.iat[0, 6] < vol2:
            return True
        else:
            return False

    def condition_a(self, T):
        pre_T = T - 3600
        df = self.datas[(self.idt == pre_T)]
        df_t = self.datas[(self.idt == T)]
        price = Decimal(df.iat[0, 1] - df.iat[0, 2]) / Decimal('2') + df.iat[0, 2]
        # HIGH(T+1)>=OPEN(T-1) - [OPEN(T-1)-CLOSE(T-1)]10%
        if df_t.iat[0, 3] < price:
            return True
        else:
            return False

    def strategy(self, T):
        if (self.condition_1(T) and self.condition_2(T)
                and self.condition_3(T) and self.condition_4(T)
                and self.condition_5(T) and self.condition_6(T)
                and self.condition_a(T)):
            # send signal
            pre_T = T - 3600
            df = self.datas[(self.idt == pre_T)]
            price = Decimal(df.iat[0, 1] - df.iat[0, 2]) / Decimal('2') + Decimal(df.iat[0, 2])
            Trader.position_judge(position=self.position, strategy_id=3, price=price, timestamp=T, trade_amount=0)
            # return True
        else:
            # 没有买卖操作
            calculator = Calculator(self.position, T, price=0, amount=0, signal=0, strategy_id=3, strategy_account_id=1)
            calculator.non_trade()
    # def run_strategy(self):
    #     df = self.datas
    #     for timestamp in df['id']:
    #         return self.strategy(timestamp)

# if __name__ == '__main__':
# buyB = BuyB(1508990400, 1509001200, 200)
# print(buyB.idt)
# sellB = SellB(1508997600, 1508990400, 1511481600, 200)
# print(sellB.filter())
# print(sellB.condition_filter())
# print(sellB.test())
# print(sellB.condition_1())
# print(sellB.condition_b(1508994000))
# print(buyB.run_strategy())
