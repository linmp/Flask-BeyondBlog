import random

from config_message import constant
from . import main
from flask import request, jsonify, current_app, session, g
from app import db, redis_store
from app.models import User, UserLoginLog, UserOperateLog
from app.utils.tool import user_login_required
from app.utils.sms import send


# 封装发送验证码
def send_sms_origin(phone):
    if not all([phone]):
        # 表示参数不完整
        return jsonify(code=4000, msg="参数不完整")
    # 判断对于这个手机号的操作，在60秒内有没有之前的记录，如果有，则认为用户操作频繁，不接受处理
    try:
        send_flag = redis_store.get("send_sms_code_%s" % phone)
    except Exception as e:
        print(e)
    else:
        if send_flag is not None:
            # 表示在60秒内之前有过发送的记录
            return jsonify(code=4001, msg="请求过于频繁，请60秒后重试")

    sms_code = random.randint(100000, 999999)  # 生成验证码

    minute = constant.Bind_PHONE_CODE_NEED  # 验证码有效时间

    # 保存真实的短信验证码
    try:
        redis_store.setex("sms_code_%s" % phone, minute * 60, sms_code)
        # 保存发送给这个手机号的记录，防止用户在60s内再次出发发送短信的操作
        redis_store.setex("send_sms_code_%s" % phone, 60, 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=4003, msg="保存短信验证码异常,请稍后在试")

    # 发送验证码
    try:
        code = send.send_sms(phone, sms_code, minute)
        if code == "Ok":
            return jsonify(code=200, msg="发送成功")
        else:
            return jsonify(code=4004, msg="发送失败")
    except Exception as e:
        print(e)
        return jsonify(code=4005, msg="发送异常")


# 发送注册验证码
@main.route("/sms", methods=["POST"])
def send_sms():
    req_json = request.get_json()
    phone = req_json.get("phone")
    if not all([phone]):
        # 表示参数不完整
        return jsonify(code=4000, msg="参数不完整")

    # 判断对于这个手机号的操作，在60秒内有没有之前的记录，如果有，则认为用户操作频繁，不接受处理
    try:
        send_flag = redis_store.get("send_sms_code_%s" % phone)
    except Exception as e:
        print(e)
    else:
        if send_flag is not None:
            # 表示在60秒内之前有过发送的记录
            return jsonify(code=4001, msg="请求过于频繁，请60秒后重试")

    # 判断手机号是否存在
    try:
        user = User.query.filter_by(phone=phone).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is not None:
            # 表示手机号已存在
            return jsonify(code=4002, msg="手机号已存在")

    return send_sms_origin(phone)


# 注册
@main.route("/register", methods=["POST"])
def register():
    """注册"""
    req_dict = request.get_json()
    phone = req_dict.get("phone")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")
    sms_code = req_dict.get("sms_code")
    phone = str(phone)
    sms_code = str(sms_code)

    # 校验参数
    if not all([phone, password, password2, sms_code]):
        return jsonify(code=400, msg="参数不完整")

    if password != password2:
        return jsonify(code=400, msg="两次密码不一致")

    # 从redis中取出短信验证码
    try:
        real_sms_code = redis_store.get("sms_code_%s" % phone)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=4001, msg="读取真实短信验证码异常")

    # 判断短信验证码是否过期
    if real_sms_code is None:
        return jsonify(code=4002, msg="短信验证码失效")

    # 删除redis中的短信验证码，防止重复使用校验
    try:
        redis_store.delete("sms_code_%s" % phone)
    except Exception as e:
        current_app.logger.error(e)

    # 判断用户填写短信验证码的正确性
    if real_sms_code != sms_code:
        return jsonify(code=4003, msg="短信验证码错误")

    # 判断用户的手机是否注册过
    try:
        user = User.query.filter_by(phone=phone).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=400, msg="数据库异常")
    else:
        if user is not None:
            # 表示已被注册
            return jsonify(code=400, msg="手机已被注册")

    # 保存用户的注册数据到数据库中
    avatar = constant.ADMIN_AVATAR_URL  # 用户头像
    user = User(username=phone, phone=phone, password=password, avatar=avatar)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=400, msg="查询数据库异常")

    # 保存登录状态到session中
    session["username"] = phone
    session["phone"] = phone
    session["user_id"] = user.id
    session["avatar"] = user.avatar

    # 返回结果
    return jsonify(code=200, msg="注册成功")


# 登录
@main.route("/login", methods=["POST"])
def login():
    """用户的登录"""
    # 获取参数
    req_dict = request.get_json()
    phone = req_dict.get("phone")
    password = req_dict.get("password")
    phone = str(phone)

    # 参数完整的校验
    if not all([phone, password]):
        return jsonify(code=400, msg="参数不完整.")

    try:
        user = User.query.filter_by(phone=phone).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=400, msg="获取用户信息失败")

    # 用数据库的密码与用户填写的密码进行对比验证
    if user is None or user.password != password:
        return jsonify(code=400, msg="用户名或密码错误")

    # 账号状态
    if not user.is_normal():
        return jsonify(code=400, msg="账号异常")

    # 添加用户登录日志
    ip_addr = request.remote_addr  # 获取用户登录的ip
    user_login_log = UserLoginLog(user_id=user.id, ip=ip_addr)
    try:
        db.session.add(user_login_log)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

    # 如果验证相同成功，保存登录状态， 在session中
    session["username"] = user.username
    session["phone"] = user.phone
    session["user_id"] = user.id
    session["avatar"] = user.avatar

    return jsonify(code=200, msg="登录成功")


# 检查登陆状态
@main.route("/session", methods=["GET"])
def check_login():
    """检查登陆状态"""
    # 尝试从session中获取用户的名字
    username = session.get("username")
    phone = session.get("phone")
    user_id = session.get('user_id')
    avatar = session.get("avatar")
    # 如果session中数据username名字存在，则表示用户已登录，否则未登录
    if username is not None:
        return jsonify(code=200, msg="true",
                       data={"username": username, "phone": phone, "user_id": user_id, "avatar": avatar})
    else:
        return jsonify(code=400, msg="用户未登录")


# 登出
@main.route("/session", methods=["DELETE"])
@user_login_required
def logout():
    """登出"""
    # 清除session数据
    session.clear()
    return jsonify(code=200, msg="成功退出登录!")


# 修改密码
@main.route("/password", methods=["PUT"])
@user_login_required
def change_password():
    """ 修改密码 """
    # 获取参数
    uid = g.user_id
    req_dict = request.get_json()
    password = req_dict.get("password")
    new_password = req_dict.get("new_password")

    # 参数完整的校验
    if not all([new_password, password, uid]):
        return jsonify(code=400, msg="参数不完整.")

    try:
        user = User.query.get(uid)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=400, msg="获取用户信息失败")

    # 用数据库的密码与用户填写的密码进行对比验证
    if user is None or user.password != password:
        return jsonify(code=400, msg="原密码密码错误")

    # 修改密码
    user.password = new_password

    # 添加用户操作日志
    ip_addr = request.remote_addr  # 获取管理员登录的ip
    operate_detail = "修改了密码"
    user_operate_log = UserOperateLog(user_id=user.id, ip=ip_addr, detail=operate_detail)
    try:
        db.session.add(user)
        db.session.add(user_operate_log)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="修改密码失败,请稍后重试!")

    return jsonify(code=200, msg="修改密码成功!")


# 发送找回密码验证码
@main.route("/reset/password/sms", methods=["POST"])
def send_find_password_sms():
    req_dict = request.get_json()
    phone = req_dict.get("phone")
    phone = str(phone)

    # 判断对于这个手机号的操作，在60秒内有没有之前的记录，如果有，则认为用户操作频繁，不接受处理
    try:
        send_flag = redis_store.get("send_sms_code_%s" % phone)
    except Exception as e:
        print(e)
    else:
        if send_flag is not None:
            # 表示在60秒内之前有过发送的记录
            return jsonify(code=4001, msg="请求过于频繁，请60秒后重试")

    # 判断账号是否存在
    try:
        user = User.query.filter_by(phone=phone).first()
    except Exception as e:
        current_app.logger.error(e)
    else:
        if user is None or not user.is_normal():
            # 账号不存在
            return jsonify(code=4002, msg="账号不存在或账号异常!")
    # 如果账号存在且正常 发送验证码
    return send_sms_origin(phone=phone)


# 找回密码
@main.route("/password", methods=["POST"])
def find_password():
    """
    发送手机号验证码
    验证成功之后就能填写个新密码
    :return:
    """
    req_dict = request.get_json()
    phone = req_dict.get("phone")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")
    sms_code = req_dict.get("sms_code")
    phone = str(phone)
    sms_code = str(sms_code)

    # 校验参数
    if not all([phone, password, password2, sms_code]):
        return jsonify(code=400, msg="参数不完整")

    if password != password2:
        return jsonify(code=400, msg="两次密码不一致")

    # 从redis中取出短信验证码
    try:
        real_sms_code = redis_store.get("sms_code_%s" % phone)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=4001, msg="读取真实短信验证码异常")

    # 判断短信验证码是否过期
    if real_sms_code is None:
        return jsonify(code=4002, msg="短信验证码失效")

    # 删除redis中的短信验证码，防止重复使用校验
    try:
        redis_store.delete("sms_code_%s" % phone)
    except Exception as e:
        current_app.logger.error(e)

    # 判断用户填写短信验证码的正确性
    if real_sms_code != sms_code:
        return jsonify(code=4003, msg="短信验证码错误")

    # 判断用户是否存在
    try:
        user = User.query.filter_by(phone=phone).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=400, msg="数据库异常")
    else:
        if user is None or not user.is_normal():
            # 不存在用户
            return jsonify(code=400, msg="用户不存在或账号异常,请注册")

    # 更改用户的密码到数据库中
    user.password = password
    try:
        # 添加用户操作日志
        ip_addr = request.remote_addr  # 获取管理员登录的ip
        operate_detail = "找回了密码"
        user_operate_log = UserOperateLog(user_id=user.id, ip=ip_addr, detail=operate_detail)
        db.session.add(user)
        db.session.add(user_operate_log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=400, msg="查询数据库异常")

    # 返回结果
    return jsonify(code=200, msg="找回密码成功!")
