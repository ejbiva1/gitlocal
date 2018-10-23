from util.Position import Position
from strategy.core.sell_a import SellA
from strategy.core.sell_b import SellB
from strategy.core.buy_b import BuyB
from strategy.core.buy_a import BuyA


def strategy_combination_b(start_time, end_time, init_balance):
    position = Position(start_date=start_time, end_date=end_time, balance=init_balance, strategy_type=3)
    dates = position.datas['id']
    print(dates.size)
    sell_b = SellB(start_time=start_time, end_time=end_time, position=position)
    buy_b = BuyB(start_time=start_time, end_time=end_time, position=position)
    for t in dates:
        sell_b.strategy(t, position)
        position = sell_b.position
        buy_b.strategy(t, position)
        position = buy_b.position


def strategy_combination_a(start_time, end_time, init_balance):
    position = Position(start_date=start_time, end_date=end_time, balance=init_balance, strategy_type=1)
    dates = position.datas['id']
    dates = dates[dates >= start_time]
    print(dates.size)
    sell_a = SellA(start_time=start_time, end_time=end_time, position=position)
    buy_a = BuyA(start_time=start_time, end_time=end_time, position=position)
    for t in dates:
        sell_a.strategy(t, position)
        position = sell_a.position
        buy_a.strategy(t, position)
        position = buy_a.position


if __name__ == '__main__':
    start_time = 1510070400
    # start_time = 1508990400
    end_time = 1510675200
    init_balance = 200000
    strategy_combination_a(start_time=start_time, end_time=end_time, init_balance=init_balance)
