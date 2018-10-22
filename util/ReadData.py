import pandas as pd
from sqlalchemy import create_engine


def read_datas_60min(startTime, endTime):
    engine = create_engine('mysql+pymysql://root:Quant123@35.162.98.89:3306/quantcoin?charset=utf8MB4')
    # 变量输入表名 table = 'btc_kline_60min'
    sql = '''
        select * from quantcoin.btc_kline_60min
        where %(start)s <= id
        and id <= %(endTime)s
        '''
    df = pd.read_sql_query(sql, params={'start': startTime, 'endTime': endTime}, con=engine, index_col='kline_id')
    return df


def read_datas_60min_test(startTime, endTime):
    engine = create_engine('mysql+pymysql://root:Quant123@35.162.98.89:3306/quantcoin?charset=utf8MB4')
    # 变量输入表名 table = 'btc_kline_60min'
    sql = '''
        select * from quantcoin.btc_kline_60min_test
        where %(start)s <= id
        and id <= %(endTime)s
        '''
    df = pd.read_sql_query(sql, params={'start': startTime, 'endTime': endTime}, con=engine, index_col='kline_id')
    return df


def read_datas_1day(startTime, endTime):
    engine = create_engine('mysql+pymysql://root:Quant123@35.162.98.89:3306/quantcoin?charset=utf8MB4')
    # 变量输入表名 table = 'btc_kline_1day'
    sql = '''
        select * from quantcoin.btc_kline_1day
        where %(start)s <= id
        and id <= %(endTime)s
        '''
    df = pd.read_sql_query(sql, params={'start': startTime - 1036800, 'endTime': endTime}, con=engine,
                           index_col='kline_id')
    return df

def read_datas_1day_test(startTime, endTime):
    engine = create_engine('mysql+pymysql://root:Quant123@35.162.98.89:3306/quantcoin?charset=utf8MB4')
    # 变量输入表名 table = 'btc_kline_1day'
    sql = '''
        select * from quantcoin.btc_kline_1day_test
        where %(start)s <= id
        and id <= %(endTime)s
        '''
    df = pd.read_sql_query(sql, params={'start': startTime - 1036800, 'endTime': endTime}, con=engine,
                           index_col='kline_id')
    return df


# todo 加入一个用户判断字段(需要连表查询确保记录唯一)
def get_trade_info(time_stamp, strategy_id, flag):
    engine = create_engine('mysql+pymysql://root:Quant123@35.162.98.89:3306/quantcoin?charset=utf8MB4')
    # todo 变量输入表名 table = 'strategy_transaction'
    sql = '''
           select * from quantcoin.strategy_transaction
           where t = %(timeStamp)s 
           and strategy_id = %(strategy_id)s
           and flag = %(flag)s 
           '''
    df = pd.read_sql_query(sql, params={'timeStamp': time_stamp, 'strategy_id': strategy_id, 'flag': flag}, con=engine,
                           index_col='strategy_transaction_id')
    return df


if __name__ == '__main__':
    # start = 1508990400
    #     # end = 1509004800
    #     # print(read_datas(start, end))
    print(get_trade_info(1508990400, 1, 0))
