from . import main
import json
from flask import request, jsonify, current_app, session
from app import db, redis_store
from app.models import User, Blog
from app.utils.tool import user_login_required


# 获取个人信息
@main.route("/profile", methods=["POST"])
def get_profile():
    """
    用户名
    性别
    头像
    个性签名
    邮箱
    注册时间
    最新上线时间
    等级
    :return:
    """
    req_json = request.get_json()
    user_id = req_json.get("user_id")

    if not user_id:
        return jsonify(re_code=400, msg="参数不完整")
    user = User.query.get(user_id)
    if not user:
        return jsonify(re_code=400, msg="查询不到用户")

    # 将数据转换为json字符串
    resp_dict = dict(re_code=200, msg="查询用户信息成功!", data=user.to_dict())
    resp_json = json.dumps(resp_dict)
    return resp_json, 200, {"Content-Type": "application/json"}


# 修改个人信息
@main.route("/profile", methods=["POST"])
@user_login_required
def change_profile():
    """
    用户名
    性别
    头像
    个性签名
    邮箱
    :return:
    """
    pass
