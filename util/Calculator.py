from decimal import Decimal


class Calculator:
    # 初始化运算器， 持仓 当前时间戳 策略执行价格 策略执行币数 策略买或卖信号(不买不卖：0，买：1，卖2
    def __init__(self, position, timestamp, price, amount, signal):
        self.T = timestamp
        self.price = price
        self.amount = amount
        self.signal = signal
        self.position = position
        self.transaction_status = None

        self.rate_of_return = 0.0000
        self.cur_rate_of_return = 0.0000

    # 策略买入
    def buy(self):
        # 基本变量
        # 初始总资产
        # pre_total = self.position.total
        pre_balance = self.position.balance
        pre_coin_cash_rate = self.position.coin_cash_rate
        pre_rate_of_return = self.rate_of_return
        # 币量
        self.position.coin_amount += self.amount
        # 持仓币价
        self.position.price = self.get_close_price()
        # 持仓余额
        self.position.balance -= Decimal(self.amount) * Decimal(self.price)
        Decimal(self.position.balance).quantize(Decimal('0.00'))
        # 总币值
        self.position.total_net_balance = Decimal(Decimal(self.position.coin_amount)
                                                  * Decimal(self.position.price)).quantize(
            Decimal('0.00'))
        self.position.total = self.position.balance + self.position.total_net_balance
        # 仓位
        self.position.coin_cash_rate = Decimal(
            Decimal(self.position.total_net_balance) / Decimal(self.position.total)).quantize('0.0000')

        # 效益计算模块
        # 总收益率（累计）
        self.rate_of_return = Decimal((Decimal(self.position.balance) - Decimal(self.position.init_balance)) / Decimal(
            self.position.init_balance)).quantize('0.0000')
        # 当期收益率（以初始本金为基准）
        # self.cur_rate_of_return = Decimal(
        #     Decimal(self.position.total - pre_total) / Decimal(self.position.total)).quantize('0.0000')
        self.cur_rate_of_return = self.rate_of_return - pre_rate_of_return

        # todo cost  由买入（卖出）实际操作决定
        self.transaction(0, None, pre_coin_cash_rate, pre_balance)

    # 策略卖出
    def sell(self):
        # 基本变量
        # 初始总资产
        # pre_total = self.position.total
        pre_balance = self.position.balance
        pre_coin_cash_rate = self.position.coin_cash_rate
        pre_rate_of_return = self.rate_of_return
        # 币量
        self.position.coin_amount -= self.amount
        # 持仓币价
        self.position.price = self.get_close_price()
        # 持仓余额
        self.position.balance += Decimal(self.amount) * Decimal(self.price)
        Decimal(self.position.balance).quantize(Decimal('0.00'))
        # 总币值
        self.position.total_net_balance = Decimal(Decimal(self.position.coin_amount)
                                                  * Decimal(self.position.price)).quantize(
            Decimal('0.00'))
        self.position.total = self.position.balance + self.position.total_net_balance
        # 仓位
        self.position.coin_cash_rate = Decimal(
            Decimal(self.position.total_net_balance) / Decimal(self.position.total)).quantize('0.0000')

        # 效益计算模块
        # 总收益率（累计）
        self.rate_of_return = Decimal((Decimal(self.position.balance) - Decimal(self.position.init_balance)) / Decimal(
            self.position.init_balance)).quantize('0.0000')
        # 当期收益率（以初始本金为基准）
        # self.cur_rate_of_return = Decimal(
        #     Decimal(self.position.total - pre_total) / Decimal(self.position.total)).quantize('0.0000')
        self.cur_rate_of_return = self.rate_of_return - pre_rate_of_return

        # todo cost  由买入（卖出）实际操作决定
        self.transaction(1, None, pre_coin_cash_rate, pre_balance)

    # 不买不卖
    def non_trade(self):
        # pre_balance = self.position.balance
        # pre_coin_cash_rate = self.position.coin_cash_rate
        pre_rate_of_return = self.rate_of_return

        # 持仓币价
        self.position.price = self.get_close_price()
        # 总币值
        self.position.total_net_balance = Decimal(Decimal(self.position.coin_amount)
                                                  * Decimal(self.position.price)).quantize(
            Decimal('0.00'))
        self.position.total = self.position.balance + self.position.total_net_balance

        # 效益计算模块
        # 总收益率（累计）
        self.rate_of_return = Decimal((Decimal(self.position.balance) - Decimal(self.position.init_balance)) / Decimal(
            self.position.init_balance)).quantize('0.0000')
        # 当期收益率（以初始本金为基准）
        # self.cur_rate_of_return = Decimal(
        #     Decimal(self.position.total - pre_total) / Decimal(self.position.total)).quantize('0.0000')
        self.cur_rate_of_return = self.rate_of_return - pre_rate_of_return

    # 获取收盘价
    def get_close_price(self):
        df = self.position.datas
        df = df[df['id'] == self.T]
        return df.iat[0, 2]

    # 买入后持久化（卖出同）[其实就是交易明细表]
    def transaction(self, flag, cost, pre_coin_cash_rate, pre_balance):
        # 买入（卖出）标志
        flag
        # 时间
        self.T
        # 价格
        cost
        # 完成前仓位
        pre_coin_cash_rate
        # 完成后仓位
        self.position.coin_cash_rate
        # 变化仓位
        position_gap = self.position.coin_cash_rate - pre_coin_cash_rate
        # 完成前余额
        pre_balance
        # 完成后余额
        self.position.balance
        # 余额变化
        balance_gap = self.position.balance - pre_balance
