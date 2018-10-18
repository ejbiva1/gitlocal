from decimal import Decimal
from util.Calculator import Calculator


class Trader:
    # judge position status
    @staticmethod
    def position_judge(position, strategy_id, price, trade_amount, timestamp):
        # buy_b strategy ==3
        if strategy_id == 3:
            if position.coin_cash_rate >= 0.8:
                return False
            elif position.coin_cash_rate <= 0.75:
                amount = Decimal(Decimal('0.05') * Decimal(position.total))
                signal = 1
                calculator = Calculator(position, timestamp, price, amount, signal, strategy_id, 1)
                calculator.buy(price)
                # todo 回写数据库交易成功字段
            #     sell_b == 4
        elif strategy_id == 4:
            signal = 0
            calculator = Calculator(position, timestamp, price, trade_amount, signal, strategy_id, 1)
            calculator.sell(price)
            # todo 回写数据库交易成功字段
        elif strategy_id == 2:
            signal = 0
            calculator = Calculator(position, timestamp, price, trade_amount, signal, strategy_id, 1)
            calculator.sell(price)
            # todo 回写数据库交易成功字段
        elif strategy_id == 1:
            signal = 1
            calculator = Calculator(position, timestamp, price, trade_amount, signal, strategy_id, 1)
            calculator.sell(price)
            # todo 回写数据库交易成功字段


