# coding:utf-8
from flask import Flask, request, session, make_response
import web.app.DB as db
import json
# import os
# import web.app.controller as controller
# from strategy import main
from facilties.functional import JsonExtendEncoder, HttpResponseModel, ResponseModel
import util.sms_chinese as sms

# from cacheout import Cache
# import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'


# cache = Cache(maxsize=256, ttl=60, timer=time.time)

@app.route('/loginWithPwd', methods=['POST'])
def login_with_pwd():
    phone = request.json.get("phoneNo")
    pwd = request.json.get("password")
    # code = request.json.get("msgCode")
    user_list = db.getUser(phone)
    if user_list:
        user = user_list.pop()
        if pwd == user.password:
            # session.permanent  = True
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


@app.route('/loginWithMsgCode', methods=['POST'])
def login_with_msg_code():
    phone = request.json.get("phoneNo")
    code = request.json.get("msgCode")
    user_list = db.getUser(phone)
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

    user_list = db.getUser(phone)
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
        user_list = db.getUser(phoneNo)
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
    phone = request.json.get('phoneNo')
    userList = db.getUser(phone)
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


#
# @app.route('/deleteUserByPhone', methods=['post'])
# def delete_user_by_phone():
#     phone = request.json.get("phone")
#
#     try:
#         result = controller.deleteStrategyLogById(phone)
#
#         result = json.dumps({"result": result.__dict__}, ensure_ascii=False, cls=JsonExtendEncoder)
#         print(result)
#         # response = HttpResponseModel(result)
#         response = make_response(result)
#         response.status = "200"
#         response.headers["Content-Type"] = "application/json"
#
#         return response
#
#     except ZeroDivisionError as e:
#         print('except:', e)


if __name__ == "__main__":
    app.run(debug=True)
