import pandas as pd
from decimal import Decimal
from util.WriteData import insert_2_strategy_transaction


class Calculator:
    # 初始化运算器， 持仓 当前时间戳 策略执行价格 策略执行币数 策略买或卖信号(不买不卖：0，买：1，卖2
    def __init__(self, position, timestamp, signal, strategy_id, strategy_account_id):
        self.T = timestamp
        # self.price = price
        # self.amount = amount
        self.signal = signal
        self.position = position
        self.transaction_status = None
        self.strategy_id = strategy_id
        self.strategy_account_id = strategy_account_id

    # 策略买入
    def buy(self, cost, amount):
        # 基本变量
        # 初始总资产
        # pre_total = self.position.total
        pre_balance = self.position.balance
        pre_balance = Decimal(str(pre_balance)).quantize(Decimal('0.00'))
        pre_current_position = self.position.current_position
        pre_rate_of_return = Decimal(self.position.rate_of_return)
        # 币量
        self.position.coin_amount += Decimal(amount)
        # 持仓币价
        self.position.price = Decimal(self.get_close_price())
        # 持仓余额
        self.position.balance -= Decimal(str(amount)) * Decimal(str(cost))
        Decimal(self.position.balance).quantize(Decimal('0.00'))
        # 总币值
        self.position.total_net_balance = Decimal(Decimal(self.position.coin_amount)
                                                  * Decimal(self.position.price)).quantize(
            Decimal('0.00'))
        self.position.total = self.position.balance + self.position.total_net_balance
        # 仓位 current_position
        self.position.current_position = Decimal(
            Decimal(self.position.total_net_balance) / Decimal(self.position.total)).quantize(Decimal('0.0000'))

        # 效益计算模块
        # 总收益率（累计） current_total_margin_rate
        self.position.rate_of_return = Decimal(
            (Decimal(self.position.total) - Decimal(self.position.init_balance)) / Decimal(
                self.position.init_balance)).quantize(Decimal('0.0000'))
        # 当期收益率（以初始本金为基准） current_margin_rate
        # self.position.cur_rate_of_return = Decimal(
        #     Decimal(self.position.total - pre_total) / Decimal(self.position.total)).quantize('0.0000')
        self.position.cur_rate_of_return = self.position.rate_of_return - pre_rate_of_return

        # cost  由买入（卖出）实际操作决定
        self.transaction(0, cost, amount, pre_current_position, pre_balance)
        print('\n')
        print('********** BUY **********')
        print('T= ' + str(self.T))
        print('amount= ' + str(Decimal(amount).quantize(Decimal('0.000000'))))
        print('price= ' + str(Decimal(cost).quantize(Decimal('0.00'))))
        print('balance= ' + str(Decimal(self.position.balance).quantize(Decimal('0.00'))))
        print('total_net_balance= ' + str(Decimal(self.position.total_net_balance).quantize(Decimal('0.00'))))
        print('total= ' + str(Decimal(self.position.total).quantize(Decimal('0.00'))))
        print('current_position= ' + str(self.position.current_position))
        print('current_margin_rate= ' + str(self.position.cur_rate_of_return))
        print('current_total_margin_rate= ' + str(self.position.rate_of_return))
        print('********** BUY **********')

    # 策略卖出
    def sell(self, cost, amount):
        # 基本变量
        # 初始总资产
        # pre_total = self.position.total
        amount = Decimal(str(amount)).quantize(Decimal('0.000000'))
        pre_balance = self.position.balance
        pre_balance = Decimal(str(pre_balance)).quantize(Decimal('0.00'))
        pre_current_position = self.position.current_position
        pre_rate_of_return = self.position.rate_of_return
        # 币量
        self.position.coin_amount -= Decimal(amount)
        # 持仓币价
        self.position.price = self.get_close_price()
        # 持仓余额
        self.position.balance += Decimal(amount) * Decimal(cost)
        Decimal(self.position.balance).quantize(Decimal('0.00'))
        # 总币值
        # self.position.total_net_balance = Decimal(Decimal(self.position.coin_amount)
        #                                           * Decimal(self.position.price)).quantize(
        #
        self.position.total_net_balance = Decimal(Decimal(self.position.coin_amount)
                                                  * Decimal(self.position.price)).quantize(
            Decimal('0.00'))
        self.position.total = self.position.balance + self.position.total_net_balance
        # 仓位
        self.position.current_position = Decimal(
            Decimal(self.position.total_net_balance) / Decimal(self.position.total)).quantize(Decimal('0.0000'))

        # 效益计算模块
        # 总收益率（累计）
        self.position.rate_of_return = Decimal(
            (Decimal(self.position.total) - Decimal(self.position.init_balance)) / Decimal(
                self.position.init_balance)).quantize(Decimal('0.0000'))
        # 当期收益率（以初始本金为基准）
        # self.position.cur_rate_of_return = Decimal(
        #     Decimal(self.position.total - pre_total) / Decimal(self.position.total)).quantize('0.0000')
        self.position.cur_rate_of_return = self.position.rate_of_return - Decimal(pre_rate_of_return)

        # cost  由买入（卖出）实际操作决定
        self.transaction(flag=1, cost=cost, amount=amount, pre_current_position=pre_current_position,
                         pre_balance=pre_balance)
        print('\n')
        print('********** SELL **********')
        print('T= ' + str(self.T))
        print('amount= ' + str(Decimal(amount).quantize(Decimal('0.000000'))))
        print('cost= ' + str(Decimal(cost).quantize(Decimal('0.00'))))
        print('balance= ' + str(Decimal(self.position.balance).quantize(Decimal('0.00'))))
        print('total_net_balance= ' + str(Decimal(self.position.total_net_balance).quantize(Decimal('0.00'))))
        print('total= ' + str(Decimal(self.position.total).quantize(Decimal('0.00'))))
        print('current_position= ' + str(self.position.current_position))
        print('current_margin_rate= ' + str(self.position.cur_rate_of_return))
        print('current_total_margin_rate= ' + str(self.position.rate_of_return))
        print('********** SELL **********')

    # 不买不卖
    def non_trade(self):
        # pre_balance = self.position.balance
        # pre_current_position = self.position.current_position
        pre_rate_of_return = self.position.rate_of_return

        # 持仓币价
        self.position.price = self.get_close_price()
        # 总币值
        self.position.total_net_balance = Decimal(Decimal(self.position.coin_amount)
                                                  * Decimal(self.position.price)).quantize(
            Decimal('0.00'))
        self.position.total = self.position.balance + self.position.total_net_balance

        # 效益计算模块
        # 总收益率（累计）
        self.position.rate_of_return = Decimal(
            (Decimal(self.position.total) - Decimal(self.position.init_balance)) / Decimal(
                float(self.position.init_balance))).quantize(Decimal('0.0000'))
        # 当期收益率（以初始本金为基准）
        # self.position.cur_rate_of_return = Decimal(
        #     Decimal(self.position.total - pre_total) / Decimal(self.position.total)).quantize('0.0000')
        self.position.cur_rate_of_return = self.position.rate_of_return - Decimal(pre_rate_of_return)
        print('\n')
        print('********** non_trade **********')
        print('T= ' + str(self.T))
        print('balance= ' + str(Decimal(self.position.balance).quantize(Decimal('0.00'))))
        print('total_net_balance= ' + str(Decimal(self.position.total_net_balance).quantize(Decimal('0.00'))))
        print('total= ' + str(Decimal(self.position.total).quantize(Decimal('0.00'))))
        print('current_position= ' + str(self.position.current_position))
        print('current_margin_rate= ' + str(self.position.cur_rate_of_return))
        print('current_total_margin_rate= ' + str(self.position.rate_of_return))
        print('********** non_trade **********')

    # 获取收盘价
    def get_close_price(self):
        df = self.position.datas
        df = df[df['id'] == self.T]
        close = df.iat[0, 2]
        close = Decimal(str(close))
        return close

    # 买入后持久化（卖出同）[其实就是交易明细表]
    def transaction(self, flag, cost, amount, pre_current_position, pre_balance):
        # # 买入（卖出）标志
        # flag
        # # 时间
        # self.T
        # # 价格
        # cost
        # # 完成前仓位
        # pre_current_position
        # # 完成后仓位
        # self.position.current_position
        # # 变化仓位
        position_gap = self.position.current_position - pre_current_position
        # # 完成前余额
        # pre_balance
        # # 完成后余额
        # self.position.balance
        # # 余额变化
        balance_gap = Decimal(str(self.position.balance)) - pre_balance

        data = {
            'strategy_account_id': [1],
            # todo 'strategy_account_id': [self.strategy_account_id],
            't': [self.T],
            'cost': [cost],
            'volumn': [amount],
            # todo 手续费暂时为0
            'commission': [0.00],
            'pre_position': [pre_current_position],
            'post_position': [self.position.current_position],
            'position_gap': [position_gap],
            'pre_balance': [pre_balance],
            'post_balance': [self.position.balance],
            'balance_gap': [balance_gap],
            'flag': [flag],
            'strategy_id': [self.strategy_id]}
        df = pd.DataFrame(data)
        insert_2_strategy_transaction(df)

    # 回写每次交易结果到表strategy_account
    def transaction_result_write_back(self):
        # todo
        return 0
