# coding:utf-8

from urllib import parse, request
import random
import time
from cacheout import Cache

cache = Cache(maxsize=256, ttl=300, timer=time.time)


def send_sms(phone_no):
    url = 'http://utf8.api.smschinese.cn'
    user_name = "cxd2017"
    key = "43a486aebdcd6d294107"
    # smsMob = '18201716178'
    smsMob = phone_no
    code = random_code()
    smsText = "DXC科技,验证码：" + code
    textmod = {'Uid': user_name, "Key": key,
               "smsMob": smsMob, "smsText": smsText}
    # json串数据使用
    # textmod = json.dumps(textmod).encode(encoding='gbk')
    # 普通数据使用
    textmod = parse.urlencode(textmod).encode(encoding='utf-8')
    print(textmod)
    header_dict = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}

    req = request.Request(url=url, data=textmod, headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    print(res)
    print(res.decode(encoding='utf-8'))
    if res.decode(encoding='utf-8') == '1':
        cache.set(smsMob, code)
        return code
    else:
        return 0


def random_code():
    code = ''
    for i in range(4):
        a = random.randint(0, 9)
        code += str(a)
    return code


if __name__ == '__main__':
    print(send_sms(18201708589))
