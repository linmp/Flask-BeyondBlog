from . import admin
from flask import request, jsonify, current_app, session
from app.models import Admin
from app.utils.tool import admin_login_required


# 登录
@admin.route("/login", methods=["POST"])
def login():
    """用户的登录"""
    # 获取参数
    req_dict = request.get_json()
    username = req_dict.get("username")
    password = req_dict.get("password")

    # 校验参数
    # 参数完整的校验
    if not all([username, password]):
        return jsonify(re_code=400, msg="参数不完整")

    try:
        admin_info = Admin.query.filter_by(username=username).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(re_code=400, msg="获取用户信息失败")

    # 用数据库的密码与用户填写的密码进行对比验证
    if admin_info is None or admin_info.password != password:
        return jsonify(re_code=400, msg="用户名或密码错误")

    # 如果验证相同成功，保存登录状态， 在session中
    session["username"] = admin_info.username
    session["admin_id"] = admin_info.id
    session["avatar"] = admin_info.avatar_url

    return jsonify(re_code=200, msg="登录成功")


# 检查登陆状态
@admin.route("/session", methods=["GET"])
def check_login():
    """检查登陆状态"""
    # 尝试从session中获取用户的名字
    username = session.get("username")
    admin_id = session.get('admin_id')
    avatar = session.get("avatar")
    # 如果session中数据username名字存在，则表示用户已登录，否则未登录
    if username is not None:
        return jsonify(re_code=200, msg="true",
                       data={"username": username, "admin_id": admin_id, "avatar": avatar})
    else:
        return jsonify(re_code=400, msg="用户未登录")


# 登出
@admin.route("/session", methods=["DELETE"])
@admin_login_required
def logout():
    """登出"""
    # 清除session数据
    session.clear()
    return jsonify(re_code=200, msg="成功退出登录!")
