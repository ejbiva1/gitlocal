# coding:utf-8
from decimal import Decimal

import sys

sys.path.append('..')
import util.ReadData as ReadData


class MidDayHighFreq:
    def __init__(self, base_price, portion, step_percent, cur_position, start_time, end_time, init_balance):
        # 基准价X
        self.base_price = base_price
        # 份数N
        self.portion = portion
        # 步长Y
        self.step_percent = step_percent
        # 当前持有份数S
        self.cur_position = cur_position
        # self.init_balance = init_balance
        # 现金余额M
        self.balance = init_balance
        self.start_time = start_time
        self.end_time = end_time
        self.data = ReadData.read_datas_5min_test(start_time, end_time)
        self.idt = self.data['id']
        self.idt = self.idt[self.idt >= start_time]
        self.dict = dict()
        # 每次交易份数
        self.portion_per_time = cur_position // portion
        temp = self.data[self.data['id'] == start_time]
        first_close_t = temp.iat[0, 2]
        temp = self.data[self.data['id'] == end_time]
        end_close_t = temp.iat[0, 2]
        self.total_init = first_close_t * cur_position + init_balance
        self.end_total = end_close_t * cur_position + init_balance

        # 发出信号

    #
    def strategy(self, start_time):
        last_signal_close_t = 0
        for t in self.idt:
            df = self.data[self.data['id'] == t]
            # df_pre = self.data[self.data['id'] == t - 300]
            # close(t)较 基准值 变化比率
            close_t = df.iat[0, 2]
            # close_t_pre = df_pre.iat[0, 2]
            # 计算出当前价格较基准价格浮动的百分比
            percent = (close_t / self.base_price) - 1
            # log(gap, self.step_percent)
            # 基准值变化比率与步长 倍率（浮动倍率）
            # ratio = percent % Decimal(str(self.step_percent))
            if percent != 0:
                ratio = abs(percent) // self.step_percent * (percent / abs(percent))
            else:
                ratio = 1
            # 与上一次达到信号点相比的趋势
            flag = self.judge_trend(close_t, last_signal_close_t, t, start_time)
            if abs(ratio) >= 1:
                last_signal_close_t = close_t

            # 涨 且倍率在整数倍
            if flag > 0 and abs(ratio) >= 1:
                print('****** sell signal *******')
                self.printSignal(close_t)
                # amount = 0
                if self.cur_position >= self.portion_per_time:
                    if ratio > 0:
                        if self.dict.get(ratio + ratio) is not None:
                            amount = self.dict[ratio + ratio]
                            self.sell(close_t, amount)
                            # 字典中的部分释放
                            self.dict.pop(ratio + ratio)
                        else:
                            amount = self.portion_per_time
                            self.sell(close_t, amount)
                    elif ratio < 0:
                        if self.dict.get(ratio - ratio) is not None:
                            amount = self.dict[ratio - ratio]
                            self.sell(close_t, amount)
                            # 字典中的部分释放
                            self.dict.pop(ratio - ratio)
                        else:
                            amount = self.portion_per_time
                            self.sell(close_t, amount)

            # 跌
            elif flag < 0 and abs(ratio) >= 1:
                print('****** buy signal *******')
                cost = self.printSignal(close_t)
                if cost <= self.balance:
                    self.buy(cost, close_t, ratio)
        return self.end_total / self.total_init - 1

    def printSignal(self, close_t):
        cost = self.portion_per_time * close_t
        print('price： ' + str(close_t))
        print('portion： ' + str(self.portion_per_time))
        print('cost： ' + str(cost))
        print('**************')
        return cost

        # 价格增减标识 1：涨， -1：跌

    def judge_trend(self, close_t, last, t, start_time):
        flag = 0
        if t == start_time:
            if close_t > self.base_price:
                flag = 1
            elif close_t < self.base_price:
                flag = -1
        else:
            # 价格增减标识
            if close_t > last and last is not 0:
                flag = 1
            elif close_t < last:
                flag = -1
        return flag

    # 实现交易 仓位调整、余额调整
    def buy(self, cost, close_t, ratio):
        self.balance -= cost
        self.cur_position += self.portion_per_time
        print('********* buy *********')
        print('price: ' + str(close_t))
        print('ratio: ' + str(ratio))
        # todo 记录买入对应的刻度
        if ratio > 0:
            if self.dict.get(ratio + ratio) is None:
                self.dict[ratio + ratio] = self.portion_per_time
            else:
                self.dict[ratio + ratio] += self.portion_per_time
        elif ratio < 0:
            if self.dict.get(ratio - ratio) is None:
                self.dict[ratio - ratio] = self.portion_per_time
            else:
                self.dict[ratio - ratio] += self.portion_per_time
        self.calculator(close_t)

    def sell(self, close_t, amount):
        # todo 卖出的刻度和价格（k-v卖出）
        # 持仓卖出
        self.cur_position -= amount
        self.balance += (close_t * amount)
        print('********* sell *********')
        print('price ' + str(close_t))
        print('amount ' + str(amount))
        self.calculator(close_t)

    def calculator(self, close_t):
        # 计算当期收益率
        cur_total = self.balance + self.cur_position * close_t
        percent = Decimal(cur_total / self.total_init - 1).quantize(Decimal('0.0000'))
        print('cur_margin: ' + str(percent))


if __name__ == '__main__':
    start_time = 1509033600
    end_time = 1523990400
    # end_time = 1509037200
    init_balance = 100000
    base_price = 8751.75
    # base_price = 5850

    portion = 5
    step_percent = 0.02
    cur_position = 10
    mid = MidDayHighFreq(base_price, portion, step_percent, cur_position, start_time, end_time, init_balance)
    no_strategy_margin = mid.strategy(start_time)
    print('no_strategy_margin: ' + str(no_strategy_margin))
