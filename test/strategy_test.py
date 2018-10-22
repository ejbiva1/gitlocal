from util.Position import Position
from strategy.core.sell_b import SellB
from strategy.core.buy_b import BuyB

start_time = 1508990400
end_time = 1512586800
init_balance = 200000

# todo type define
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
