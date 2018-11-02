from util.ReadData import *
import decimal
from util.Trader import *
from entity.Signal import Signal


class SellB:
    # todo 定义全局的strategy_id
    # 初始化策略参数
    def __init__(self, start_time, end_time, position):
        self.start_time = start_time
        self.end_time = end_time
        # self.T = timestamp
        # self.balance = balance
        # self.init_balance = balance
        # self.pre_T = timestamp - 3600
        # self.next_T = timestamp + 3600

        # self.summary = rep.Summary()
        self.position = position
        self.datas = position.datas
        self.idt = self.datas['id']
        self.price = 0.00
        self.trade_amount = 0.000000

    # # 获取[ T + (-)1 ]时间区间的数据
    # def filter(self):
    #     df = self.datas
    #     df = df[(df['id'] >= self.pre_T)]
    #     df = df[(df['id'] <= self.next_T)]
    #     return df

    def condition_1(self, T):
        df = self.datas[(self.idt == T)]
        df = df[(df['close'] > df['open'])]
        if df.empty:
            return False
        else:
            return True

    def condition_2(self, T):
        pre_T = T - 3600
        df1 = self.datas[(self.idt == T)]
        df2 = self.datas[(self.idt == pre_T)]
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
        df1 = self.datas[(self.idt == T)]
        df2 = self.datas[(self.idt == pre_T)]
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
        df1 = self.datas[(self.idt == T)]
        df2 = self.datas[(self.idt == pre_T)]
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
        df1 = self.datas[(self.idt == T)]
        df2 = self.datas[(self.idt == next_T)]
        # high is at row[4] (from 0-7 ,begin with id not kline_id)
        if df2.iat[0, 4] >= decimal.Decimal(df1.iat[0, 2]) * decimal.Decimal('1.02'):
            return True
        else:
            return False

    def condition_b(self, T):
        pre_T = T - 3600
        next_T = T + 3600
        df1 = self.datas[(self.idt == pre_T)]
        df2 = self.datas[(self.idt == next_T)]
        diff = decimal.Decimal(df1.iat[0, 1] - df1.iat[0, 2]) * decimal.Decimal('0.1')
        # HIGH(T+1)>=OPEN(T-1) - [OPEN(T-1)-CLOSE(T-1)]10%
        if df2.iat[0, 4] >= (decimal.Decimal(df1.iat[0, 1]) - diff):
            return True
        else:
            return False

    def condition_c(self, T):
        # LOW(T+1)< 买入价格95%，则决策卖出，卖出价格为买入价格95%，卖出仓位=T日买入仓位
        df = get_trade_info(T, 3, 0)
        next_T = T + 3600
        df2 = self.datas[(self.idt == next_T)]
        if df.empty:
            return False
        elif Decimal(df2.iat[0, 3]) < Decimal(df.iat[0, 2]) * Decimal('0.95'):
            self.price = df.iat[0, 2]
            self.trade_amount = df.iat[0, 3]
            return True
        else:
            # self.price = df.iat[0, 2]
            self.trade_amount = df.iat[0, 3]
            return False

    def condition_0(self, T):
        df = get_trade_info(T - 3600, strategy_id=3, flag=0)
        if not df.empty:
            # price = df.iat[0, 2]
            current_position = self.position.current_position
            if 0.75 <= current_position <= 0.8:
                return True
            else:
                return False
        else:
            return False

    def strategy(self, T, position):
        signal = Signal(flag=0, signal=0)
        self.position = position
        calculator = Calculator(self.position, T, signal=0, strategy_id=4, strategy_account_id=1)
        if self.condition_0(T):
            # 前提是已经在T日执行了短线策略1（BUY-B），即已经以价格P买入并仓位已经到达75%~80%
            if (self.condition_1(T) and self.condition_2(T)
                    and self.condition_3(T) and self.condition_4(T)):

                if self.condition_a(T):
                    # 卖出仓位=T日买入仓位，卖出价格为CLOSE(T)1.02
                    df = get_trade_info(T, 3, 0)
                    df1 = self.datas[(self.idt == T)]
                    price = Decimal(df1.iat[0, 2]) * Decimal('1.02')
                    if df.empty:
                        pass
                    else:
                        print_signal(T, price, amount=df.iat[0, 3], reason='condition_a')
                        signal.signal = 2
                        position_check = Trader.position_judge(position=self.position,
                                                               strategy_id=4, calculator=calculator, price=price,
                                                               trade_amount=df.iat[0, 3])
                        if position_check is not 0:
                            signal.flag = 1

                    # return True
                else:
                    if self.condition_b(T):
                        # 则卖出价格为OPEN(T-1) - [OPEN(T-1)-CLOSE(T-1)]10%。卖出仓位=T日买入仓位
                        df = get_trade_info(T, 3, 0)
                        pre_T = T - 3600
                        df1 = self.datas[(self.idt == pre_T)]
                        open_price = df1.iat[0, 1]
                        close_price = df1.iat[0, 2]
                        gap = (Decimal(open_price) - Decimal(close_price)) * Decimal('0.1')
                        price = Decimal(open_price) - gap
                        if df.empty:
                            pass
                        else:
                            print_signal(T, price, amount=df.iat[0, 3], reason='condition_b')
                            signal.signal = 2
                            position_check = Trader.position_judge(position=self.position, calculator=calculator,
                                                                   strategy_id=4, price=price,
                                                                   trade_amount=df.iat[0, 3])
                            if position_check is not 0:
                                signal.flag = 1
                        # return True
                    else:
                        if self.condition_c(T):
                            # 卖出价格为买入价格95%，卖出仓位=T日买入仓位
                            print_signal(T, self.price, amount=self.trade_amount, reason='condition_c true')
                            signal.signal = 2
                            position_check = Trader.position_judge(position=self.position,
                                                                   strategy_id=4, price=self.price,
                                                                   calculator=calculator,
                                                                   trade_amount=self.trade_amount)
                            if position_check == 0:
                                calculator.non_trade()
                            else:
                                signal.flag = 1
                            # return True
                        else:
                            # 卖出价格为CLOSE(T+1)，卖出仓位=T日买入仓位
                            next_T = T + 3600
                            df = self.datas[(self.idt == next_T)]
                            print_signal(T, df.iat[0, 2], amount=self.trade_amount, reason='condition_c false')
                            signal.signal = 2
                            position_check = Trader.position_judge(position=self.position,
                                                                   strategy_id=4, price=df.iat[0, 2],
                                                                   calculator=calculator,
                                                                   trade_amount=self.trade_amount)
                            if position_check is not 0:
                                signal.flag = 1

            else:
                # 卖出价格为CLOSE(T+1)，卖出仓位=T日买入仓位
                df = get_trade_info(T - 3600, 3, 0)
                next_T = T + 3600
                df2 = self.datas[(self.idt == next_T)]
                if df.empty:
                    pass
                else:
                    print_signal(T, df2.iat[0, 2], amount=df.iat[0, 3], reason='nor condition_1-4')
                    signal.signal = 2
                    position_check = Trader.position_judge(position=self.position,
                                                           strategy_id=4, price=df2.iat[0, 2], calculator=calculator,
                                                           trade_amount=df.iat[0, 3])
                    if position_check is not 0:
                        signal.flag = 1

        else:
            print('condition_0 False: no_trade')
            self.call_no_trade(T, calculator)

        self.position = calculator.position
        return signal

    # 更新CLOSE(T+1)，T日买入仓位 到self中的trade_amount，price
    def refresh_price_amount(self, T):
        df = get_trade_info(T - 3600, 3, 0)
        next_T = T + 3600
        df2 = self.datas[(self.idt == next_T)]
        self.price = df2.iat[0, 2]
        if not df.empty:
            self.trade_amount = df.iat[0, 3]

    # call
    def call_no_trade(self, T, calculator):
        # 没有买卖操作
        # calculator = Calculator(self.position, T, signal=0, strategy_id=4, strategy_account_id=1)
        calculator.non_trade()


def print_signal(T, price, amount, reason):
    print('********** SIGNAL **********')
    print('signal_type= sell_b')
    print('signal_reason= ' + str(reason))
    print('price= ' + str(price))
    print('amount= ' + str(amount))
    print('timestamp= ' + str(T))
    print('********** SIGNAL **********')
# def run_strategy(self):
#     df = self.datas
#     for timestamp in df['id']:
#         return self.strategy(timestamp)
#     # 卖出结算
#     Trader.sell()


# if __name__ == '__main__':
#     sellB = SellB(1508990400, 1509001200, 200)
# sellB = SellB(1508997600, 1508990400, 1511481600, 200)
# print(sellB.filter())
# print(sellB.condition_filter())
# print(sellB.test())
# print(sellB.condition_1())
# print(sellB.condition_b(1508994000))
# print(sellB.run_strategy())
