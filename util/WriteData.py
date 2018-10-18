import pandas as pd
from sqlalchemy import create_engine


def insert_2_strategy_transaction(dataframe):
    engine = create_engine('mysql+pymysql://root:Quant123@35.162.98.89:3306/quantcoin?charset=utf8MB4')
    dataframe.to_sql('strategy_transaction', engine, index=False, if_exists='append')
    print('insert successfully')


if __name__ == '__main__':
    # start = 1508990400
    #     # end = 1509004800
    #     # print(read_datas(start, end))
    # print(get_trade_info(1508990400, 1, 0))
    data = {'strategy_account_id': [1, 2, 3],
            't': [1508990400, 1508994000, 1508997600],
            'cost': [7.929392, 7.929392, 7.929392],
            'volumn': [0.9, 1, 2.1],
            'commission': [0.00, 0.00, 0.00],
            'pre_position': [0, 0.90, 1.90],
            'post_position': [90, 80, 85],
            'position_gap': [90, 80, 85],
            'pre_balance': [90, 80, 85],
            'post_balance': [90, 80, 85],
            'balance_gap': [90, 80, 85],
            'flag': [1, 0, 1],
            'strategy_id': [0, 1, 0]}
    df = pd.DataFrame(data)
    insert_2_strategy_transaction(df)
