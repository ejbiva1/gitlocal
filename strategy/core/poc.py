# def poc_strategy(t, sell_dict, buy_dict, data):


def sell_signal(t, sell_dict, data):
    df = data[data['id'] == t]
    s1 = close_t_1(df, sell_dict)
    s2 = open_t_1(df, sell_dict)
    s3 = high_t_1(df, sell_dict)
    s4 = low_t_1(df, sell_dict)
    s5 = close_t_2(df, sell_dict)
    s6 = open_t_2(df, sell_dict)
    s7 = high_t_2(df, sell_dict)
    s8 = low_t_2(df, sell_dict)
    if s1 and s2 and s3 and s4 and s5 and s6 and s7 and s8:
        # todo 卖出信号
        return 0


def buy_signal(t, buy_dict, data):
    df = data[data['id'] == t]
    b1 = close_t_1(df, buy_dict)
    b2 = open_t_1(df, buy_dict)
    b3 = high_t_1(df, buy_dict)
    b4 = low_t_1(df, buy_dict)
    b5 = close_t_2(df, buy_dict)
    b6 = open_t_2(df, buy_dict)
    b7 = high_t_2(df, buy_dict)
    b8 = low_t_2(df, buy_dict)
    if b1 and b2 and b3 and b4 and b5 and b6 and b7 and b8:
        # todo 买入信号
        return 0


def low_t_2(df, dict):
    if dict['low(T-2)'] is not 0:
        x = df.iat[0, 3]
        flag = eval(dict['low(T-1)'])
        return flag


def high_t_2(df, dict):
    if dict['high(T-2)'] is not 0:
        x = df.iat[0, 4]
        flag = eval(dict['high(T-1)'])
        return flag


def open_t_2(df, dict):
    if dict['open(T-2)'] is not 0:
        x = df.iat[0, 1]
        flag = eval(dict['open(T-1)'])
        return flag


def close_t_2(df, dict):
    if dict['close(T-2)'] is not 0:
        x = df.iat[0, 2]
        flag = eval(dict['close(T-1)'])
        return flag


def low_t_1(df, dict):
    if dict['low(T-1)'] is not 0:
        x = df.iat[0, 3]
        flag = eval(dict['low(T-1)'])
        return flag


def high_t_1(df, dict):
    if dict['high(T-1)'] is not 0:
        x = df.iat[0, 4]
        flag = eval(dict['high(T-1)'])
        return flag


def open_t_1(df, dict):
    if dict['open(T-1)'] is not 0:
        x = df.iat[0, 1]
        flag = eval(dict['open(T-1)'])
        return flag


def close_t_1(df, dict):
    if dict['close(T-1)'] is not 0:
        x = df.iat[0, 2]
        flag = eval(dict['close(T-1)'])
        return flag
