# coding:utf-8

from flask import Flask, request, session, make_response
import DB as db
import json
import os

# from strategy import main
# from facilties.functional import JsonExtendEncoder, HttpResponseModel
from flask import Flask, Blueprint, render_template, request, redirect, jsonify
from facilties.functional import JsonExtendEncoder, HttpResponseModel, ResponseModel

import controller as controller
# 用户模块
import DB as db
from facilties.functional import JsonExtendEncoder, HttpResponseModel, ResponseModel
import sys

sys.path.append('../../util')
import util.sms_chinese as sms

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'


@app.route('/startStrategy', methods=['POST'])
def startStrategy():
    strategyId = request.json.get("strategyId")
    startTime = request.json.get("startTime")
    endTime = request.json.get("endTime")
    initBalance = request.json.get("initBalance")
    coinCategory = request.json.get("coinCategory")
    if 1000000 >= initBalance >= 10000:
        controller.startStartStrategy(strategyId, initBalance, startTime, endTime)
        return make_response(json.dumps({'result': 'strategy started'}))
    else:
        return make_response(json.dumps({'result': 'pls be sure initBalance is correct'}))


@app.route('/loadLogList', methods=['POST'])
def loadLogList():
    strategy_log_list = []
    session.permanent = True
    session['userId'] = 1

    strategy_id = request.json.get('strategy_id')
    if strategy_id is None:
        strategy_id = 0

    strategyLogList = controller.loadLogList(session['userId'], strategy_id)
    for item in strategyLogList:
        strategy_log_list.append(item.__dict__)
    result = json.dumps({"list": strategy_log_list}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/getLogDetail/<int:strategyLogId>', methods=['post'])
def getLogDetail(strategyLogId):
    session.permanent = True
    session['userId'] = 1
    log_details = controller.getLogDetail(strategyLogId, session['userId'])

    result = json.dumps({'list': log_details.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return result


# 保存并执行 策略
@app.route('/saveStrategyConf', methods=['post'])
def saveStrategyConf():
    session.permanent = True
    session['userId'] = 1

    strategy_name = request.json.get("strategy_name")
    strategy_id = request.json.get("strategy_id")
    start_time = request.json.get("start_time")
    end_time = request.json.get("end_time")
    init_balance = request.json.get("init_balance")
    strategyConfItemlist = request.json.get("strategyConfItemlist")
    coin_category = request.json.get("coin_category")
    strategy_oper = request.json.get('strategy_oper')

    regression_result = controller.saveStrategyAndRun(strategy_id=strategy_id,
                                                      strategy_name=strategy_name,
                                                      userId=session['userId'],
                                                      init_balance=init_balance,
                                                      start_time=start_time,
                                                      end_time=end_time,
                                                      coin_category=coin_category,
                                                      strategyConfItemlist=strategyConfItemlist,
                                                      strategy_oper=strategy_oper)

    response = make_response(
        json.dumps({'result': regression_result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/getALLStrategy', methods=['post'])
def getALLStrategy():
    strategy_list = []
    session.permanent = True
    session['userId'] = 1
    strategyList = controller.getALLStrategy(session['userId'])
    for item in strategyList:
        strategy_list.append(item.__dict__)
    result = json.dumps({"list": strategy_list}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/getStrategyDetail', methods=['post'])
def getStrategyDetail():
    strategy_id = request.json.get('strategy_id')
    session.permanent = True
    session['userId'] = 1
    strategy = controller.getStrategyDetail(creator=session['userId'], strategy_id=strategy_id)

    result = json.dumps({"result": strategy.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/checkStrategyName', methods=['post'])
def checkStrategyName():
    session.permanent = True
    session['userId'] = 1

    strategy_id = request.json.get("strategy_id")
    if strategy_id is None:
        strategy_id = 0
    strategy_name = request.json.get("strategy_name")
    is_strategy_name_exist = controller.checkStrategyName(strategy_name=strategy_name, creator=session['userId'],
                                                          strategy_id=strategy_id)

    result = json.dumps({"result": is_strategy_name_exist.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/saveStrategyName', methods=['post'])
def saveStrategyName():
    session.permanent = True
    session['userId'] = 1

    strategy_name = request.json.get("strategy_name")
    strategy_id = request.json.get("strategy_id")
    result = controller.saveStrategyName(strategy_name=strategy_name, strategy_id=strategy_id,
                                         creator=session['userId'])

    result = json.dumps({"result": result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/deleteStrategyLogById', methods=['post'])
def deleteStrategyLogById():
    strategy_log_id = request.json.get("strategy_log_id")

    try:
        result = controller.deleteStrategyLogById(strategy_log_id)

        result = json.dumps({"result": result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
        # response = HttpResponseModel(result)
        response = make_response(result);
        response.status = "200"
        response.headers["Content-Type"] = "application/json"

        return response

    except ZeroDivisionError as e:
        print('except:', e)


@app.route('/getStrategy', methods=['post'])
def getStrategy():
    strategy_id = request.json.get('strategy_id')
    session.permanent = True
    session['userId'] = 1

    try:

        strategy_confs = controller.getStrategy(creator=session['userId'], strategyId=strategy_id)

        result = json.dumps({"result": strategy_confs.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)

        response = make_response(result)
        response.status = "200"
        response.headers["Content-Type"] = "application/json"

        return response

    except ZeroDivisionError as e:
        print('except:', e)


# 暂存 或  新添加 策略
@app.route('/saveStrategyConfOrUpdate', methods=['post'])
def saveStrategy():
    session.permanent = True
    session['userId'] = 1
    strategy_id = request.json.get('strategy_id')
    print(strategy_id)
    if strategy_id is None:
        strategy_id = 0
    strategy_name = request.json.get("strategy_name")
    start_time = request.json.get("start_time")
    end_time = request.json.get("end_time")
    init_balance = request.json.get("init_balance")
    strategy_conf_item_list = request.json.get("strategyConfItemlist")
    coin_category = request.json.get("coin_category")
    strategy_oper = request.json.get("strategy_oper")

    result = controller.saveStrategyConfOrUpdate(
        strategy_id=strategy_id,
        strategy_name=strategy_name,
        userId=session['userId'],
        init_balance=init_balance,
        start_time=start_time,
        end_time=end_time,
        coin_category=coin_category,
        strategyConfItemlist=strategy_conf_item_list, strategy_oper=strategy_oper)
    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/executeStrategy', methods=['post'])
def executeStrategy():
    session.permant = True
    session['userId'] = 1
    strategy_id = request.json.get('strategy_id')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    create_time = request.json.get('create_time')
    coin_category = request.json.get('coin_category')
    init_balance = request.json.get('init_balance')

    result = controller.mob_executeStrategy(userId=session['userId'], strategy_id=strategy_id,
                                            start_time=start_time, create_time=create_time,
                                            end_time=end_time, init_balance=init_balance,
                                            coin_category=coin_category)

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


# 诗丽 手机端 调用 该接口， 执行poc 并返回相应历史数据；
@app.route('/mob_executeStrategy', methods=['post'])
def mob_executeStrategy():
    # session.permant = True
    session['userId'] = 1
    strategy_id = request.json.get('strategy_id')
    create_time = request.json.get('create_time')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    init_balance = request.json.get('init_balance')
    coin_category = request.json.get('coin_category')

    result = controller.mob_executeStrategy(userId=session['userId'], strategy_id=strategy_id, start_time=start_time,
                                            end_time=end_time, create_time=create_time, init_balance=init_balance,
                                            coin_category=coin_category)

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


# 诗丽 手机端 调用 该接口， 获取策略 回测历史数据
@app.route('/mob_strategytradehistory', methods=['post'])
def mob_strategytradehistory():
    session.permant = True
    session['userId'] = 1

    strategy_log_id = request.json.get('strategy_log_id')

    result = controller.mob_strategy_trade_history(strategy_log_id=strategy_log_id)

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


# 诗丽 手机端 调用 该接口， 获取我的策略列表 策略名称 最后一次调用时间 总的调用次数
@app.route('/mob_getMyStrategyList', methods=['post'])
def mob_get_my_strategy_list():
    session.permant = True
    session['userId'] = 1
    result = controller.mob_my_strategy_list(userId=session['userId'])

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


# 诗丽 手机端 调用 该接口， 获取某个策略回测列表 每次执行的结果 （策略名称，回测时间，策略收益率，基准收益率，最大回撤）
@app.route('/mob_getStrategyLogList', methods=['post'])
def mob_get_strategy_log_list():
    session.permant = True
    session['userId'] = 1
    strategy_id = request.json.get('strategy_id')
    result = controller.mob_get_strategy_log_list(strategy_id=strategy_id, user_id=session['userId'])

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


# 删除策略 del_strategy
@app.route('/delStrategy', methods=['post'])
def delStrategy():
    session.permant = True
    session['userId'] = 1

    strategy_id = request.json.get('strategy_id')
    result = controller.deleteStrategyById(strategy_id=strategy_id, userId=session['userId'])

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


# 用户模块
@app.route('/loginWithPwd', methods=['POST'])
def login_with_pwd():
    phone = request.json.get("phoneNo")
    pwd = request.json.get("password")
    # code = request.json.get("msgCode")
    user_list = db.getUserByPhone(phone)
    if user_list:
        user = user_list.pop()
        if pwd == user.password:
            # session.permant = True
            session['userId'] = user.user_id
            session['phoneNo'] = user.phone
            data = {'login': 'Successed'}
            result = ResponseModel(data=data, code='1', message='登录成功！')
            response = makeResp(result)
        else:
            data = {'login': 'Failed'}
            result = ResponseModel(data=data, code='0', message='登录失败,用户密码不匹配！')
            response = makeResp(result)
    else:
        data = {'login': 'Failed'}
        result = ResponseModel(data=data, code='0', message='登录失败,该手机号未注册！')
        response = makeResp(result)
    return response


#
# @app.route('/getUserDetail', methods=['post'])
# def get_user_detail():
#     phone = request.json.get('phoneNo')
#     userList = db.getUser(phone)
#     user = userList.pop()
#     result = json.dumps({"result": user.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
#     response = make_response(result)
#     response.status = "200"
#     response.headers["Content-Type"] = "application/json"
#     return response


def makeResp(result):
    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/getAllStrategyName', methods=['post'])
def getAllStrategyName():
    session.permant = True
    session['userId'] = 1
    result = controller.get_all_strategy_name(creator=session['userId'])
    result = json.dumps({"result": result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/getDefaultStrategyName', methods=['post'])
def getDefaultStrategyName():
    session.permant = True
    session['userId'] = 1
    # set default strategy name
    default_strategy_name = controller.set_default_strategy_name(creator=session['userId'])
    result = json.dumps({"result": default_strategy_name.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


# 诗丽 手机端 调用 该接口， 获取回测图标数据
@app.route('/mob_getDataArrays', methods=['post'])
def mob_get_data_array():
    # session.permant = True
    # session['userId'] = 1
    strategy_log_id = request.json.get('strategy_log_id')
    result = controller.mob_get_strategy_account_list(strategy_log_id=strategy_log_id)

    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"

    return response


#
# # 用户模块
# @app.route('/loginWithPwd', methods=['POST'])
# def login_with_pwd():
#     phone = request.json.get("phoneNo")
#     pwd = request.json.get("password")
#     # code = request.json.get("msgCode")
#     user_list = db.getUser(phone)
#     if user_list:
#         user = user_list.pop()
#         if pwd == user.password:
#             # session.permanent  = True
#             session['userId'] = user.user_id
#             session['phoneNo'] = user.phone
#             data = {'login': 'Successed'}
#             result = ResponseModel(data=data, code='1', message='登录成功！')
#             response = makeResp(result)
#         else:
#             data = {'login': 'Failed'}
#             result = ResponseModel(data=data, code='0', message='登录失败,用户密码不匹配！')
#             response = makeResp(result)
#     else:
#         data = {'login': 'Failed'}
#         result = ResponseModel(data=data, code='0', message='登录失败,该手机号未注册！')
#         response = makeResp(result)
#     return response


@app.route('/loginWithMsgCode', methods=['POST'])
def login_with_msg_code():
    phone = request.json.get("phoneNo")
    code = request.json.get("msgCode")
    user_list = db.getUserByPhone(phone)
    if user_list:
        user = user_list.pop()
        cache_code = sms.cache.get(phone)
        if code == cache_code:
            # session.permant = True
            session['userId'] = user.user_id
            session['phoneNo'] = user.phone
            data = {'login': 'Successed'}
            result = ResponseModel(data=data, code='1', message='登录成功！')
            response = makeResp(result)
        else:
            data = {'login': 'Failed'}
            result = ResponseModel(data=data, code='0', message='登录失败,验证码不匹配！')
            response = makeResp(result)
    else:
        data = {'login': 'Failed'}
        result = ResponseModel(data=data, code='0', message='登录失败,该手机号未注册！')
        response = makeResp(result)
    return response


@app.route('/sendMSG', methods=['POST'])
def send_msg():
    phone = request.json.get("phoneNo")
    if sms.send_sms(phone) != 0:
        data = {'sendMsg': 'Successed'}
        result = ResponseModel(data=data, code='1', message='发送成功！请在1分钟内完成验证。')
        response = makeResp(result)
    else:
        data = {'sendMsg': 'Failed'}
        result = ResponseModel(data=data, code='0', message='发送失败，请稍后再试。')
        response = makeResp(result)

    return response


def makeResp(result):
    response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
    response = make_response(response)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/signUp', methods=['POST'])
def sign_up():
    phone = request.json.get("phoneNo")
    pwd = request.json.get("password")
    code = request.json.get("msgCode")
    nick_name = request.json.get("nickName")
    open_id = request.json.get("openId")
    age = request.json.get("age")
    gender = request.json.get("gender")
    avator = request.json.get("avatar")
    levels = request.json.get("levels")
    strategy_amount = request.json.get("strategyAmount")
    history_amount = request.json.get("historyAmount")
    style = request.json.get("style")
    experience = request.json.get("experience")

    user_list = db.getUserByPhone(phone)
    if not user_list:
        # user = user_list.pop()
        cache_code = sms.cache.get(phone)
        if code == cache_code:
            db.saveUserItem(phone, pwd, nick_name, open_id, age, gender, avator, levels,
                            strategy_amount, history_amount, style, experience)
            data = {'signUp': 'Successed'}
            result = ResponseModel(data=data, code='1', message='注册成功！')
            response = makeResp(result)
        else:
            data = {'signUp': 'Failed'}
            result = ResponseModel(data=data, code='0', message='注册失败,验证码不匹配！')
            response = makeResp(result)
    else:
        data = {'signUp': 'Failed'}
        result = ResponseModel(data=data, code='0', message='注册失败,该手机号已存在！')
        response = makeResp(result)
    return response


# todo
@app.route('/changePwd', methods=['POST'])
def change_pwd():
    phone = request.json.get("phoneNo")
    pwd = request.json.get("password")
    code = request.json.get("msgCode")
    phoneNo = session['phoneNo']
    if not phoneNo:
        data = {'changePwd': 'Failed'}
        result = ResponseModel(data=data, code='0', message='session为空，无访问权限！')
        response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
        response = make_response(response)
        response.status = "403"
        response.headers["Content-Type"] = "application/json"
    else:
        user_id = session['userId']
        if user_id is None:
            user_id = 1
        user_list = db.getUser(user_id)
        if str(phone) == phoneNo:
            if user_list:
                # user = user_list.pop()
                cache_code = sms.cache.get(phone)
                # userList = db.getUser(phone)
                #         # user = userList.pop()
                #         # user.user_id

                if code == cache_code:
                    db.update_user_pwd(user_id=session['userId'], new_pwd=pwd)
                    data = {'changePwd': 'Successed'}
                    result = ResponseModel(data=data, code='1', message='密码修改成功！')
                    response = makeResp(result)
                else:
                    data = {'changePwd': 'Failed'}
                    result = ResponseModel(data=data, code='0', message='密码修改失败,验证码不匹配！')
                    response = makeResp(result)
            else:
                data = {'changePwd': 'Failed'}
                result = ResponseModel(data=data, code='0', message='密码修改失败,内部错误')
                response = makeResp(result)
        else:
            data = {'changePwd': 'Failed'}
            result = ResponseModel(data=data, code='0', message='密码修改失败,该手机号与预留手机号不一致！')
            response = makeResp(result)
    return response


@app.route('/getUserDetail', methods=['post'])
def get_user_detail():
    # phone = request.json.get('user_id')
    user_id = session['userId']
    if user_id is None:
        user_id = 1
    userList = db.getUser(user_id)
    user = userList.pop()
    result = json.dumps({"result": user.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
    response = make_response(result)
    response.status = "200"
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/alterPersonalInfo', methods=['POST'])
def alter_personal_info():
    user_id = session['userId']

    # phone = request.json.get("phoneNo")
    # pwd = request.json.get("password")
    # code = request.json.get("msgCode")
    nick_name = request.json.get("nickName")
    open_id = request.json.get("openId")
    age = request.json.get("age")
    gender = request.json.get("gender")
    avator = request.json.get("avatar")
    style = request.json.get("style")
    experience = request.json.get("experience")

    if user_id:
        db.update_user_info(user_id, nick_name, open_id, age, gender, avator, style, experience)
        data = {'signUp': 'Successed'}
        result = ResponseModel(data=data, code='1', message='修改成功！')
        response = makeResp(result)
    else:
        data = {'update': 'Failed'}
        result = ResponseModel(data=data, code='0', message='修改失败，无访问权限！')
        response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
        response = make_response(response)
        response.status = "403"
        response.headers["Content-Type"] = "application/json"
    return response


@app.route('/changePhoneNum', methods=['POST'])
def change_phone_num():
    user_id = session['userId']
    phone = request.json.get("phoneNo")
    code = request.json.get("msgCode")
    cache_code = sms.cache.get(phone)

    if user_id:
        if code == cache_code:
            db.update_user_phone_num(phone, user_id)
            data = {'changePhoneNum': 'Successed'}
            result = ResponseModel(data=data, code='1', message='修改成功！')
            response = makeResp(result)
        else:
            data = {'update': 'Failed'}
            result = ResponseModel(data=data, code='0', message='修改失败，验证码不匹配！')
            response = makeResp(result)
    else:
        data = {'update': 'Failed'}
        result = ResponseModel(data=data, code='0', message='修改失败，无访问权限！')
        response = make_response(json.dumps({'result': result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder))
        response = make_response(response)
        response.status = "403"
        response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run(debug=True)
