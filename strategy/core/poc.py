from entity.Poc_signal import Poc_signal
from decimal import Decimal


# def poc_strategy(t, sell_dict, buy_dict, data):


def sell_signal(t, sell_dict, data):
    df = data[data['id'] == t]
    df_1 = data[data['id'] == t - 86400]
    df_2 = data[data['id'] == t - 172800]
    s1 = close_t_1(df_1, sell_dict)
    s2 = open_t_1(df_1, sell_dict)
    s3 = high_t_1(df_1, sell_dict)
    s4 = low_t_1(df_1, sell_dict)
    s5 = close_t_2(df_2, sell_dict)
    s6 = open_t_2(df_2, sell_dict)
    s7 = high_t_2(df_2, sell_dict)
    s8 = low_t_2(df_2, sell_dict)
    s11 = close_t(df, sell_dict)
    s12 = close_t(df, sell_dict)
    s13 = close_t(df, sell_dict)
    s14 = close_t(df, sell_dict)
    s9 = ma5_t(data, sell_dict, t)
    s10 = ma10_t(data, sell_dict, t)
    if s1 and s2 and s3 and s4 and s5 and s6 and s7 and s8 and s9 and s10 and s11 and s12 and s13 and s14:
        # todo 卖出信号
        price = df.iat[0, 2]
        signal = Poc_signal(signal=2, price=Decimal(price).quantize(Decimal('0.000000')))
        return signal
    else:
        return Poc_signal(signal=0, price=0)


def buy_signal(t, buy_dict, data):
    df = data[data['id'] == t]
    df_1 = data[data['id'] == t - 86400]
    df_2 = data[data['id'] == t - 172800]
    b1 = close_t_1(df_1, buy_dict)
    b2 = open_t_1(df_1, buy_dict)
    b3 = high_t_1(df_1, buy_dict)
    b4 = low_t_1(df_1, buy_dict)
    b5 = close_t_2(df_2, buy_dict)
    b6 = open_t_2(df_2, buy_dict)
    b7 = high_t_2(df_2, buy_dict)
    b8 = low_t_2(df_2, buy_dict)
    b11 = close_t(df, buy_dict)
    b12 = close_t(df, buy_dict)
    b13 = close_t(df, buy_dict)
    b14 = close_t(df, buy_dict)
    b9 = ma5_t(data, buy_dict, t)
    b10 = ma10_t(data, buy_dict, t)
    if b1 and b2 and b3 and b4 and b5 and b6 and b7 and b8 and b9 and b10 and b11 and b12 and b13 and b14:
        # todo 买入信号
        price = df.iat[0, 2]
        signal = Poc_signal(signal=1, price=Decimal(price).quantize(Decimal('0.000000')))
        return signal
    else:
        return Poc_signal(signal=0, price=0)


def low_t_2(df, dict):
    if dict['low(T-2)'] is not 0:
        x = df.iat[0, 3]
        flag = eval(dict['low(T-2)'])
        return flag
    else:
        return True


def high_t_2(df, dict):
    if dict['high(T-2)'] is not 0:
        x = df.iat[0, 4]
        flag = eval(dict['high(T-2)'])
        return flag
    else:
        return True


def open_t_2(df, dict):
    if dict['open(T-2)'] is not 0:
        x = df.iat[0, 1]
        flag = eval(dict['open(T-2)'])
        return flag
    else:
        return True


def close_t_2(df, dict):
    if dict['close(T-2)'] is not 0:
        x = df.iat[0, 2]
        flag = eval(dict['close(T-2)'])
        return flag
    else:
        return True


def low_t_1(df, dict):
    if dict['low(T-1)'] is not 0:
        x = df.iat[0, 3]
        flag = eval(dict['low(T-1)'])
        return flag
    else:
        return True


def high_t_1(df, dict):
    if dict['high(T-1)'] is not 0:
        x = df.iat[0, 4]
        flag = eval(dict['high(T-1)'])
        return flag
    else:
        return True


def open_t_1(df, dict):
    if dict['open(T-1)'] is not 0:
        x = df.iat[0, 1]
        flag = eval(dict['open(T-1)'])
        return flag
    else:
        return True


def close_t_1(df, dict):
    if dict['close(T-1)'] is not 0:
        x = df.iat[0, 2]
        flag = eval(dict['close(T-1)'])
        return flag
    else:
        return True


def low_t(df, dict):
    if dict['low(T-1)'] is not 0:
        x = df.iat[0, 3]
        flag = eval(dict['low(T-1)'])
        return flag
    else:
        return True


def high_t(df, dict):
    if dict['high(T-1)'] is not 0:
        x = df.iat[0, 4]
        flag = eval(dict['high(T-1)'])
        return flag
    else:
        return True


def open_t(df, dict):
    if dict['open(T-1)'] is not 0:
        x = df.iat[0, 1]
        flag = eval(dict['open(T-1)'])
        return flag
    else:
        return True


def close_t(df, dict):
    if dict['close(T-1)'] is not 0:
        x = df.iat[0, 2]
        flag = eval(dict['close(T-1)'])
        return flag
    else:
        return True


def ma5_t(data, dict, t):
    if dict['ma5(T)'] is not 0:
        df = data[data['id'] <= t]
        df = df[df['id'] >= t - 345600]
        x = df['close'].mean()
        flag = eval(dict['ma5(T)'])
        return flag
    else:
        return True


def ma10_t(data, dict, t):
    if dict['ma10(T)'] is not 0:
        df = data[data['id'] <= t]
        df = df[df['id'] >= t - 777600]
        x = df['close'].mean()
        flag = eval(dict['ma10(T)'])
        return flag
    else:
        return True
