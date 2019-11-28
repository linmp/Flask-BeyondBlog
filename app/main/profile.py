from . import main
import json
from flask import request, jsonify, current_app, session, g
from app import db, redis_store
from app.models import User, Blog
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
        return jsonify(re_code=400, msg="参数不完整")
    user = User.query.get(user_id)
    if not user:
        return jsonify(re_code=400, msg="查询不到用户")

    # 将数据转换为json字符串
    resp_dict = dict(re_code=200, msg="查询用户信息成功!", data=user.to_dict())
    resp_json = json.dumps(resp_dict)
    return resp_json, 200, {"Content-Type": "application/json"}


"""
# 修改个人信息
@main.route("/profile", methods=["POST"])
@user_login_required
def change_profile():

    # 用户名
    # 性别
    # 个性签名
    # :return:


    req_json = request.get_json()
    username = req_json.get("username")
    gender = req_json.get("gender")
    info = req_json.get("info")
    user_id = session.get("user_id")

    user = User.query.get(user_id)
    if not user:
        return jsonify(re_code=400, msg="查询不到用户")

"""


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
        return jsonify(re_code=400, msg="未上传图片")

    try:
        path = "ossPath"
        file_name = upload.upload_pic(path, image_file)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(re_code=400, msg="上传图片失败")

    # 保存图片路由到数据库中
    try:
        User.query.filter_by(id=user_id).update({"avatar": file_name})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(re_code=400, msg="保存图片信息失败")

    avatar_url = file_name

    # 保存成功返回
    session["avatar"] = avatar_url
    return jsonify(re_code=200, msg="保存成功", data={"avatar": avatar_url})


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
        return jsonify(re_code=400, msg="用户名不可为空")

    # 查询数据库是否有这个用户
    find_user = User.query.filter_by(username=username).first()
    if find_user is not None:
        return jsonify(re_code=400, msg="用户名已被占用,无法执行本次修改")

    # 更新用户名到数据库中
    try:
        User.query.filter_by(id=user_id).update({"username": username})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(re_code=400, msg="更改用户名失败")

    # 保存成功返回
    session["username"] = username
    return jsonify(re_code=200, msg="保存成功", data={"username": username})


# 修改用户的简介
@main.route("/user/info", methods=["POST"])
@user_login_required
def update_user_info():
    """设置用户的头像
    参数：
    info 用户的简介 不可为空
    用户id (g.user_id)
    """

    # 装饰器的代码中已经将user_id保存到g对象中，所以视图中可以直接读取
    user_id = g.user_id

    req_json = request.get_json()
    info = req_json.get("info")

    if info is None:
        return jsonify(re_code=400, msg="个人简介参数不完整")

    # 保存文件名到数据库中
    try:
        User.query.filter_by(id=user_id).update({"info": info})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(re_code=400, msg="更改个人简介失败")

    # 保存成功返回
    return jsonify(re_code=200, msg="保存成功", data={"info": info})


# 修改用户的性别
@main.route("/user/gender", methods=["POST"])
@user_login_required
def update_user_gender():
    """
    设置用户的性别
    参数：
    gender (0,1,2) 分别是 保密 男 女
    用户id (g.user_id)
    """

    # 装饰器的代码中已经将user_id保存到g对象中，所以视图中可以直接读取
    user_id = g.user_id
    req_json = request.get_json()
    gender = req_json.get("gender")

    if gender is None:
        return jsonify(re_code=400, msg="参数不完整")

    if gender not in (0, 1, 2):
        return jsonify(re_code=400, msg="参数不正确")

    # 更新数据库
    try:
        User.query.filter_by(id=user_id).update({"gender": gender})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(re_code=400, msg="数据库失败,更改性别失败")

    # 保存成功返回
    return jsonify(re_code=200, msg="保存成功", data={"gender": gender})
