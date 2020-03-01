from . import main
import json
from flask import request, jsonify, current_app, session, g
from app import db, redis_store
from app.models import User
from app.utils.tool import user_login_required
from app.utils.alioss import upload


# 获取个人信息
@main.route("/user/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
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
    # req_json = request.get_json()
    # user_id = req_json.get("user_id")

    if not user_id:
        return jsonify(code=400, msg="参数不完整")
    user = User.query.get(user_id)
    if not user:
        return jsonify(code=400, msg="查询不到用户")

    # 将数据转换为json字符串
    resp_dict = dict(code=200, msg="查询用户信息成功!", data=user.to_dict())
    resp_json = json.dumps(resp_dict)
    return resp_json, 200, {"Content-Type": "application/json"}


# 设置用户的头像
@main.route("/user/avatar", methods=["POST"])
@user_login_required
def update_user_avatar():
    """
    设置用户的头像
    参数： 图片(多媒体表单格式)
    用户id (g.user_id)
    """

    # 装饰器的代码中已经将user_id保存到g对象中，所以视图中可以直接读取
    user_id = g.user_id

    # 获取图片
    image_file = request.files.get("avatar")

    if image_file is None:
        return jsonify(code=400, msg="未上传图片")

    try:
        path = "ossPath"
        file_name = upload.upload_pic(path, image_file)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=400, msg="上传图片失败")

    # 保存图片路由到数据库中
    try:
        User.query.filter_by(id=user_id).update({"avatar": file_name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=400, msg="保存图片信息失败")

    avatar_url = file_name

    # 保存成功返回
    session["avatar"] = avatar_url
    return jsonify(code=200, msg="保存成功", data={"avatar": avatar_url})


# 修改用户的用户名
@main.route("/user/username", methods=["POST"])
@user_login_required
def update_username():
    """
    设置用户的用户名
    参数：
    username 要更改的用户名
    用户id (g.user_id)
    """

    # 装饰器的代码中已经将user_id保存到g对象中，所以视图中可以直接读取
    user_id = g.user_id

    req_json = request.get_json()
    username = req_json.get("username")

    if username is None:
        return jsonify(code=400, msg="用户名不可为空")

    # 查询数据库是否有这个用户
    find_user = User.query.filter_by(username=username).first()
    if find_user is not None:
        return jsonify(code=400, msg="用户名已被占用,无法执行本次修改")

    # 更新用户名到数据库中
    try:
        User.query.filter_by(id=user_id).update({"username": username})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(code=400, msg="更改用户名失败")

    # 保存成功返回
    session["username"] = username
    return jsonify(code=200, msg="保存成功", data={"username": username})