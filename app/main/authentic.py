from . import main
from flask import request, jsonify, current_app, session
from app import db, redis_store
from app.models import User, UserLoginLog, UserOperateLog
from app.utils.tool import user_login_required


# 注册
@main.route("/register", methods=["POST"])
def register():
    """注册"""
    # 获取请求的json数据，返回字典
    req_dict = request.get_json()
    email = req_dict.get("email")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")
    image_code = req_dict.get("image_code")
    image_code_id = req_dict.get("image_code_id")

    # 校验参数
    if not all([email, password, password2, image_code, image_code_id]):
        return jsonify(re_code=400, msg="参数不完整")

    # 业务逻辑处理
    # 从redis中取出真实的图片验证码
    try:
        real_image_code = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(re_code=400, msg="redis数据库异常")

    # 判断图片验证码是否过期
    if real_image_code is None:
        # 表示图片验证码没有或者过期
        return jsonify(re_code=400, msg="图片验证码失效,请刷新重新输入")

    # 删除redis中的图片验证码，防止用户使用同一个图片验证码验证多次
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    # 与用户填写的值进行对比
    if real_image_code.decode() != image_code.lower():
        # 表示用户填写错误
        return jsonify(re_code=400, msg="图片验证码错误")

    if password != password2:
        return jsonify(re_code=400, msg="两次密码不一致")

    # 判断用户的邮箱是否注册过
    try:
        user = User.query.filter_by(email=email).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(re_code=400, msg="数据库异常")
    else:
        if user is not None:
            # 表示邮箱已被注册
            return jsonify(re_code=400, msg="邮箱已被注册")

    # 保存用户的注册数据到数据库中
    user = User(username=email, email=email)

    user.password = password  # 设置属性

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(re_code=400, msg="查询数据库异常")

    # 保存登录状态到session中
    session["username"] = email
    session["email"] = email
    session["user_id"] = user.id

    # 返回结果
    return jsonify(re_code=200, msg="注册成功")


# 登录
@main.route("/login", methods=["POST"])
def login():
    """用户的登录"""
    # 获取参数
    req_dict = request.get_json()
    email = req_dict.get("email")
    password = req_dict.get("password")

    # 校验参数
    # 参数完整的校验
    if not all([email, password]):
        return jsonify(re_code=400, msg="参数不完整.")

    try:
        user = User.query.filter_by(email=email).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(re_code=400, msg="获取用户信息失败")

    # 用数据库的密码与用户填写的密码进行对比验证
    if user is None or user.password != password:
        return jsonify(re_code=400, msg="用户名或密码错误")

    # 添加用户登录日志
    ip_addr = request.remote_addr  # 获取用户登录的ip
    user_login_log = UserLoginLog(user_id=user.id, ip=ip_addr)
    try:
        db.session.add(user_login_log)
        db.session.commit()
    except:
        db.session.rollback()

    # 如果验证相同成功，保存登录状态， 在session中
    session["username"] = user.username
    session["email"] = user.email
    session["user_id"] = user.id
    session["avatar"] = user.avatar

    return jsonify(re_code=200, msg="登录成功")


# 检查登陆状态
@main.route("/session", methods=["GET"])
def check_login():
    """检查登陆状态"""
    # 尝试从session中获取用户的名字
    username = session.get("username")
    email = session.get("email")
    user_id = session.get('user_id')
    avatar = session.get("avatar")
    # 如果session中数据username名字存在，则表示用户已登录，否则未登录
    if username is not None:
        return jsonify(re_code=200, msg="true",
                       data={"username": username, "email": email, "user_id": user_id, "avatar": avatar})
    else:
        return jsonify(re_code=400, msg="用户未登录")


# 登出
@main.route("/session", methods=["DELETE"])
@user_login_required
def logout():
    """登出"""
    # 清除session数据
    session.clear()
    return jsonify(re_code=200, msg="成功退出登录!")


# 修改密码
@main.route("/password", methods=["PUT"])
@user_login_required
def change_password():
    """ 修改密码 """
    # 获取参数
    req_dict = request.get_json()
    username = session.get("username")
    password = req_dict.get("password")
    new_password = req_dict.get("new_password")

    # 校验参数
    # 参数完整的校验
    if not all([new_password, password,username]):
        return jsonify(re_code=400, msg="参数不完整.")

    try:
        user = User.query.filter_by(username=username).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(re_code=400, msg="获取用户信息失败")

    # 用数据库的密码与用户填写的密码进行对比验证
    if user is None or user.password != password:
        return jsonify(re_code=400, msg="原密码密码错误")

    # 修改密码
    user.password = new_password

    # 添加用户操作日志
    ip_addr = request.remote_addr  # 获取管理员登录的ip
    operate_detail = "用户id:%r 用户名:%s,修改了密码" % (user.id, username)
    user_operate_log = UserOperateLog(user_id=user.id, ip=ip_addr, detail=operate_detail)
    try:
        db.session.add(user)
        db.session.add(user_operate_log)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(re_code=400, msg="修改密码失败,请稍后重试!")

    return jsonify(re_code=200, msg="修改密码成功!")


# 找回密码
@main.route("/password", methods=["POST"])
def find_password():
    pass