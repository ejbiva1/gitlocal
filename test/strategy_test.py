from util.Position import Position
from strategy.core.sell_a import SellA
from strategy.core.sell_b import SellB
from strategy.core.buy_b import BuyB
from strategy.core.buy_a import BuyA
from util.WriteData import *
from decimal import Decimal


# todo type define
def strategy_combination_b(start_time, end_time, init_balance):
    # 写入strategy_log表
    # todo get creator from token
    new_log = Log(strategy_id=3, start_date=start_time, end_date=end_time, init_balance=init_balance,
                  coin_category='btc', creator=1)
    log_id = insert_2_strategy_log(new_log)
    position = Position(start_date=start_time, end_date=end_time, balance=init_balance, strategy_type=3)
    dates = position.datas['id']
    print(dates.size)
    sell_b = SellB(start_time=start_time, end_time=end_time, position=position)
    buy_b = BuyB(start_time=start_time, end_time=end_time, position=position)
    for t in dates:
        status = 0
        sell_flag = sell_b.strategy(t, position)
        position = sell_b.position
        if sell_flag.flag is not 0:
            status = 1
            # todo signal 策略中的信号放到一个对象返回到这里
        account_id_sell = account_insert(position=position, t=t, strategy_log_id=log_id, signal=int(sell_flag.signal),
                                         transaction_status=status)
        buy_flag = buy_b.strategy(t, position)
        position = buy_b.position
        # strategy_account 写入
        if buy_flag.flag is not 0:
            status = 2
            # todo signal 策略中的信号放到一个对象返回到这里
        account_id_buy = account_insert(position=position, t=t, strategy_log_id=log_id, signal=int(buy_flag.signal),
                                        transaction_status=status)

    # 回写策略执行后总资产到strategy_log表
    write_back2log(position, log_id)


def strategy_combination_a(start_time, end_time, init_balance):
    # 写入strategy_log表
    new_log = Log(strategy_id=1, start_date=start_time, end_date=end_time, init_balance=init_balance,
                  coin_category='btc', creator=1)
    log_id = insert_2_strategy_log(new_log)
    position = Position(start_date=start_time, end_date=end_time, balance=init_balance, strategy_type=1)
    dates = position.datas['id']
    dates = dates[dates >= start_time]
    print(dates.size)
    sell_a = SellA(start_time=start_time, end_time=end_time, position=position)
    buy_a = BuyA(start_time=start_time, end_time=end_time, position=position)
    for t in dates:
        status = 0
        sell_flag = sell_a.strategy(t, position)
        position = sell_a.position
        if sell_flag.flag is not 0:
            status = 1
            # todo signal 策略中的信号放到一个对象返回到这里
        account_id_sell = account_insert(position=position, t=t, strategy_log_id=log_id, signal=int(sell_flag.signal),
                                         transaction_status=status)
        buy_flag = buy_a.strategy(t, position)
        position = buy_a.position
        if buy_flag is not 0:
            status = 2
            # todo signal 策略中的信号放到一个对象返回到这里
        account_id_buy = account_insert(position=position, t=t, strategy_log_id=log_id, signal=int(buy_flag.signal),
                                        transaction_status=status)

    #  回写策略执行后总资产到strategy_log表
    write_back2log(position, log_id)


def account_insert(position, t, strategy_log_id, signal, transaction_status):
    df = position.datas[position.datas['id'] == t]
    open_price = Decimal(df.iat[0, 1]).quantize(Decimal('0.00'))
    close = Decimal(df.iat[0, 2]).quantize(Decimal('0.00'))
    low = Decimal(df.iat[0, 3]).quantize(Decimal('0.00'))
    high = Decimal(df.iat[0, 4]).quantize(Decimal('0.00'))
    cost = Decimal(position.price).quantize(Decimal('0.00'))
    current_cash_balance = Decimal(position.balance).quantize(Decimal('0.00'))
    current_position = Decimal(position.current_position).quantize(Decimal('0.000000'))
    new_account = Account(strategy_log_id=strategy_log_id, current_cash_balance=current_cash_balance,
                          current_coin_balance=position.coin_amount, cost=cost,
                          total_net_balance=position.total_net_balance, current_net_value=position.total,
                          current_total_margin_rate=position.rate_of_return,
                          current_margin_rate=position.cur_rate_of_return,
                          current_position=current_position, signal=signal,
                          transaction_status=transaction_status, t=t,
                          open=open_price, close=close, high=high, low=low)
    account_id = insert_2_strategy_account(new_account=new_account)
    return account_id


def write_back2log(position, log_id):
    total = position.total
    log = Log(strategy_log_id=log_id, final_margin=total)
    update_strategy_log(log)


if __name__ == '__main__':
    # start_time = 1510070400
    start_time = 1508990400
    # end_time = 1510675200
    end_time = 1509022800
    init_balance = 200000
    strategy_combination_b(start_time=start_time, end_time=end_time, init_balance=init_balance)
