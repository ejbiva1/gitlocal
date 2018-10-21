from decimal import Decimal
from util.Calculator import Calculator


class Trader:
    # judge position status
    @staticmethod
    def position_judge(position, strategy_id, price, trade_amount, timestamp):
        # buy_b strategy ==3
        if strategy_id == 3:
            if position.current_position >= 0.8:
                return 0
            elif 0.7 < position.current_position <= 0.75:
                exception_buy = Decimal('0.05') * Decimal(position.total)
                if exception_buy > position.balance:
                    amount = Decimal(position.balance) / Decimal(price)
                else:
                    amount = Decimal(exception_buy) / Decimal(price)
                signal = 1
                calculator = Calculator(position, timestamp, price, amount, signal, strategy_id, 1)
                calculator.buy(price)
                # todo 回写数据库交易成功字段
                return amount
            #     sell_b == 4
            else:
                buy_rate = str(Decimal('0.8') - position.current_position)
                exception_buy = Decimal(buy_rate) * Decimal(position.total)
                if exception_buy > position.balance:
                    amount = Decimal(position.balance) / Decimal(price)
                else:
                    amount = Decimal(exception_buy) / Decimal(price)
                signal = 1
                calculator = Calculator(position, timestamp, price, amount, signal, strategy_id, 1)
                calculator.buy(price)
                # todo 回写数据库交易成功字段
                return amount
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
