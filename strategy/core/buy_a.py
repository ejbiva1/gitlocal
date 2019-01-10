# coding:utf-8
import sys

sys.path.append('..')
from util.Position import Position
from util.Trader import *
from entity.Signal import Signal


# todo 判断是否能取到MA10(T-2),取不到，则不返回信号
# todo NON trade 不需要每次在策略里做，而是在每个周期做一次就好了
class BuyA:
    # 初始化策略参数
    def __init__(self, start_time, end_time, position):
        self.start_time = start_time
        self.end_time = end_time
        self.datas = position.datas
        self.idt = self.datas['id']
        self.position = position
        self.pre_MA5 = 0.000000
        self.MA5 = 0.000000
        self.pre_MA10 = 0.000000
        self.MA10 = 0.000000

    def condition_1(self, T):
        pre_T = T - 86400
        pre_2T = T - 172800
        df = self.datas[(self.idt == pre_T)]
        df1 = self.datas[(self.idt == pre_2T)]
        if df1.iat[0, 2] < self.MA5 and df.iat[0, 2] > self.pre_MA5:
            return True
        else:
            return False

    def condition_2(self):
        if self.MA5 > self.MA10:
            return True
        else:
            return False

    def condition_3(self):
        if self.MA5 > self.pre_MA5 and self.MA10 > self.pre_MA10:
            return True
        else:
            return False

    def condition_a(self, T):
        pre_T = T - 86400
        df = self.datas[(self.idt == pre_T)]
        try:
            if df.iat[0, 3] <= Decimal(df.iat[0, 2]) * Decimal('1.02'):
                return True
            else:
                return False
        except IndexError:
            return False

    def strategy(self, T, position):
        self.position = position
        self.update_MA(T)
        self.update_pre_MA(T)
        flag = 0
        signal = Signal(flag=0, signal=0)
        calculator = Calculator(self.position, T, signal=0, strategy_id=1, strategy_account_id=1)
        if (self.condition_a(T) and self.condition_1(T)
                and self.condition_2() and self.condition_3()):
            # send signal
            pre_T = T - 86400
            df = self.datas[(self.idt == pre_T)]
            # 价格是否为 CLOSE（T-1）
            price = df.iat[0, 2]
            print('********** SIGNAL **********')
            print('signal_type= buy_a ,')
            print('price= ' + str(price))
            print('timestamp= ' + str(T))
            print('********** SIGNAL **********')
            signal.signal = 1
            position_check = Trader.position_judge(position=self.position, strategy_id=1, price=price,
                                                   calculator=calculator,
                                                   trade_amount=0)
            if position_check == 0:
                calculator.non_trade()
            signal.flag = 1
        else:
            # 没有买卖操作
            calculator.non_trade()
        self.position = calculator.position
        return signal

    # get MA5(T-1) MA10(T-1）
    def update_MA(self, T):
        start_timestamp_5T = T - 5 * 86400
        start_timestamp_10T = T - 10 * 86400
        pre_T = T - 86400
        df_5 = self.datas[(self.idt >= start_timestamp_5T)]
        df1_5 = df_5[df_5['id'] < pre_T]
        df_10 = self.datas[(self.idt >= start_timestamp_10T)]
        df1_10 = df_10[df_10['id'] < pre_T]

        self.MA5 = df1_5['close'].mean()
        self.MA10 = df1_10['close'].mean()

    # get MA5(T-1) MA10(T-1）
    def update_pre_MA(self, T):
        start_timestamp_5T = T - 6 * 86400
        start_timestamp_10T = T - 11 * 86400
        pre_T = T - 2 * 86400
        df_5 = self.datas[(self.idt >= start_timestamp_5T)]
        df1_5 = df_5[df_5['id'] < pre_T]
        df_10 = self.datas[(self.idt >= start_timestamp_10T)]
        df1_10 = df_10[df_10['id'] < pre_T]

        self.pre_MA5 = df1_5['close'].mean()
        self.pre_MA10 = df1_10['close'].mean()


if __name__ == '__main__':
    pos = Position(1509984000, 1515600000, 200, 1)
    buy_a = BuyA(1509984000, 1515600000, pos)
    buy_a.update_MA(1514995200)
