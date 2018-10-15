from decimal import Decimal


class Calculator:
    # 初始化运算器， 持仓 当前时间戳 策略执行价格 策略执行币数 策略买或卖信号(不买不卖：0，买：1，卖2
    def __init__(self, position, timestamp, price, amount, signal):
        self.T = timestamp
        self.price = price
        self.amount = amount
        self.signal = signal
        self.position = position

        self.rate_of_return = 0.0000
        self.cur_rate_of_return = 0.0000


    # 策略买入
    def buy(self):
        # 基本变量
        # 初始总资产
        pre_total = self.position.total
        pre_rate_of_return = self.rate_of_return
        # 币量
        self.position.coin_amount += self.amount
        # 持仓币价
        self.position.price = self.get_close_price()
        # 持仓余额
        self.position.balance -= Decimal(self.amount) * Decimal(self.price)
        Decimal(self.position.balance).quantize(Decimal('0.00'))
        # 总币值
        self.position.coin_total = Decimal(Decimal(self.position.coin_amount)
                                           * Decimal(self.position.price)).quantize(
            Decimal('0.00'))
        self.position.total = self.position.balance + self.position.coin_total

        # 效益计算模块
        # 总收益率（累计）
        self.rate_of_return = Decimal((Decimal(self.position.balance) - Decimal(self.position.init_balance)) / Decimal(
            self.position.init_balance)).quantize('0.0000')
        # 当期收益率（以初始本金为基准）
        # self.cur_rate_of_return = Decimal(
        #     Decimal(self.position.total - pre_total) / Decimal(self.position.total)).quantize('0.0000')
        self.cur_rate_of_return = self.rate_of_return - pre_rate_of_return
        # 买入后持久化（卖出同）
        # 买入标志（卖出）
        # 时间
        # 价格
        # 完成前仓位
        # 完成后仓位
        # 变化仓位
        # 完成前余额
        # 完成后余额
        # 余额变化

    # 策略卖出
    def sell(self):
        return 0

    # 不买不卖

    # 获取收盘价
    def get_close_price(self):
        df = self.position.datas
        df = df[df['id'] == self.T]
        return df.iat[0, 2]

    # 现金金额
    def balance_cal(self):
        return 0

    # 持仓量
    def coin_amount_cal(self):
        return self.position.coin_total

    # 持仓总金额
    def coin_total_value_cal(self):
        return Decimal(self.position.coin_total) * Decimal(self.position.price)

    # 仓位
    def position_rate_cal(self):
        return 0

    # 总资产(T)
    def total_asset_cal(self):
        return 0

    # 总收益率
    def rate_of_return_cal(self):
        return 0

    # 当期收益率
    def cur_rate_of_return_cal(self):
        return 0

    # 数据持久化
    def insert(self):
        return 0
