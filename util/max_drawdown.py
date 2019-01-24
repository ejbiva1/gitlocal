import numpy as np


def max_drawdown(timeseries):
    """
    获取最大回撤率
    :param timeseries:(收益率列表)
    :return:最大回撤率
    """
    # 回撤结束时间点
    i = np.argmax(np.maximum.accumulate(timeseries) - timeseries)
    # 回撤开始的时间点
    j = np.argmax(timeseries[:i])
    return (float(timeseries[i]) / timeseries[j]) - 1.

#
# import numpy as np
# import matplotlib.pyplot as plt
#
# x = [100, 200, 50, 300, 150, 100, 200]
# # np.maximum.accumulate(x) 执行后 结果为：[100, 200, 200, 300, 300, 300, 300]
# # np.maximum.accumulate(x) - x 为：[0, 0, 150, 0, 50, 200, 100]
# # np.argmax() 为找数组中最大的值的下标位置 故此 200 位置为5
# j = np.argmax(np.maximum.accumulate(x) - x)
# # print('j is {j}'.format(j=j))
# i = np.argmax(x[:j])
# # print('i is {i}'.format(i=i))
# d = x[i] - x[j]
# # print(d)
# plt.plot(x)
# plt.plot([i, j], [x[i], x[j]],
#          'o', color='Red', markersize=10)
# plt.show()
