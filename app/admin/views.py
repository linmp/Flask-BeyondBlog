from . import admin
from app import db
from app.utils.tool import admin_login_required
from app.models import Board, AdminOperateLog, Admin, Tag, User
from config_message.constant import ADMIN_AVATAR_URL
from flask import g, request, jsonify, session


# 新增标签
@admin.route("/tag", methods=["POST"])
@admin_login_required
def add_tag():
    admin_id = g.admin_id
    json_data = request.get_json()
    ip_addr = request.remote_addr
    tag = json_data.get("tag")
    if not all([ip_addr, tag]):
        return jsonify(code=4001, msg="参数不完整")

    try:
        # 添加标签
        t = Tag(name=tag)
        detail = "添加了新标签: %s " % tag
        admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
        db.session.add(t)
        db.session.add(admin_operate_log)
        db.session.commit()
        return jsonify(code=200, msg="新增标签成功")
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify(code=4004, msg="新增标签失败")


# 删除标签
@admin.route("/tag", methods=["DELETE"])
@admin_login_required
def delete_tag():
    admin_id = g.admin_id
    json_data = request.get_json()
    ip_addr = request.remote_addr
    tag = json_data.get("tag")
    if not all([ip_addr, tag]):
        return jsonify(code=4001, msg="参数不完整")
    try:
        # 删除标签
        t = Tag.query.filter_by(name=tag).delete()
        detail = "删除了旧标签: %s " % tag
        admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
        db.session.add(admin_operate_log)
        db.session.commit()
        return jsonify(code=200, msg="删除标签成功")
    except Exception as e:
        print(e)
        return jsonify(code=4004, msg="删除标签失败")


# 新增管理员
@admin.route("/manager", methods=["POST"])
@admin_login_required
def add_manager():
    """
    需要的用户信息
        管理员用户名
        管理员密码
        权限 管理员 超级管理员
    注意:
        管理员只能创建权限比自己小的子管理员
    :return:
    """
    admin_id = g.admin_id
    ip_addr = request.remote_addr  # 获取管理员登录的ip
    req_dict = request.get_json()
    new_admin_username = req_dict.get("username")
    new_admin_password = req_dict.get("password")

    # 参数完整的校验
    if not all([new_admin_username, new_admin_password, ip_addr]):
        return jsonify(code=400, msg="参数不完整")

    # 获取当前管理员的信息
    current_admin = Admin.query.get(admin_id)
    if not current_admin:
        return jsonify(code=400, msg="当前管理员出错")

    # 获取当前管理员的权限
    current_admin_power = current_admin.power

    # 判断管理员是否是超级管理员
    if current_admin_power == "超级管理员":
        new_admin = Admin(username=new_admin_username, password=new_admin_password, power="管理员",
                          avatar=ADMIN_AVATAR_URL)
        try:
            db.session.add(new_admin)
            detail = "添加了新管理员: %s " % new_admin_username
            admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
            db.session.add(admin_operate_log)
            db.session.commit()
            return jsonify(code=200, msg="添加管理员成功")
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify(code=400, msg="保存数据失败,或许用户名冲突,请稍后再试")
    else:
        return jsonify(code=400, msg="当前管理员无法添加此权限用户")


# 删除管理员
@admin.route("/manager", methods=["DELETE"])
@admin_login_required
def delete_manager():
    """
    需要的用户信息
        管理员用户名
    :return:
    """
    admin_id = g.admin_id
    admin_name = session.get("username")  # 获取管理员的名字
    ip_addr = request.remote_addr  # 获取管理员登录的ip
    req_dict = request.get_json()
    delete_admin_username = req_dict.get("username")

    # 参数完整的校验
    if not all([delete_admin_username, ip_addr]):
        return jsonify(code=400, msg="参数不完整")

    # 获取当前管理员的信息
    current_admin = Admin.query.get(admin_id)
    if not current_admin:
        return jsonify(code=400, msg="当前管理员出错")

    # 获取当前管理员的权限
    current_admin_power = current_admin.power
    if current_admin_power != "超级管理员":
        return jsonify(code=400, msg="当前管理员权利不够删除管理员")

    # 执行操作
    if current_admin_power == "超级管理员":
        delete_admin = Admin.query.filter_by(username=delete_admin_username).first()
        if not delete_admin:
            return jsonify(code=400, msg="查询不到将要删除的管理员")

        # 如果删除的是自己
        if delete_admin.username == admin_name:
            return jsonify(code=400, msg="不能删除自己信息")

        try:
            delete_admin.status = "删除"
            db.session.add(delete_admin)
            detail = "删除了管理员: %s " % delete_admin_username
            admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
            db.session.add(admin_operate_log)
            db.session.commit()
            return jsonify(code=200, msg="删除管理员成功!")

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify(code=400, msg="执行操作失败")
    return jsonify(code=400, msg="未知错误")


# 屏蔽用户
@admin.route("/user/status", methods=["DELETE"])
@admin_login_required
def delete_user():
    """
    用户的用户名
    :return:
    """
    admin_id = g.admin_id
    ip_addr = request.remote_addr  # 获取管理员登录的ip
    req_dict = request.get_json()
    delete_user_username = req_dict.get("username")

    # 参数完整的校验
    if not all([delete_user_username, ip_addr]):
        return jsonify(code=400, msg="参数不完整")

    user = User.query.filter(username=delete_user_username).first()
    if user is None:
        return jsonify(code=400, msg="查询不到用户")

    try:
        user.status = "删除"
        db.session.add(user)
        detail = "屏蔽了用户: %s " % user
        admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
        db.session.add(admin_operate_log)
        db.session.commit()
        return jsonify(code=200, msg="删除用户成功!")

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="执行操作失败")


# 删除评论
@admin.route("/comment", methods=["DELETE"])
def delete_comment():
    pass


# 更改背景
@admin.route("/background", methods=["POST"])
def change_background():
    pass


# 发送公告
@admin.route("/bulletin/board", methods=["POST"])
@admin_login_required
def bulletin_board():
    admin_id = g.admin_id  # 获取管理员的id
    ip_addr = request.remote_addr  # 获取管理员登录的ip
    req_dict = request.get_json()
    title = req_dict.get("title")
    content = req_dict.get("content")

    # 校验参数
    # 参数完整的校验
    if not all([title, content, ip_addr]):
        return jsonify(code=400, msg="参数不完整")

    # 将数据保存
    board = Board(title=title, content=content, admin_id=admin_id)

    try:
        detail = "发送了新公告: %s " % title
        admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
        db.session.add(board)
        db.session.add(admin_operate_log)
        db.session.commit()
        return jsonify(code=200, msg="保存数据成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="保存数据失败")


# 统计浏览量
@admin.route("/views/numbers", methods=["POST"])
def views_numbers_count():
    pass


# 查看所有用户略情
@admin.route("/all/data/user", methods=["POST"])
def all_user_message():
    pass


# 查看所有的反馈信息
@admin.route("/feedback", methods=["POST"])
def feed_back():
    pass


# 活跃人数
@admin.route("/login/numbers", methods=["POST"])
def login_numbers():
    pass


# 发博总数
@admin.route("/blog/numbers", methods=["POST"])
def blog_numbers():
    pass


# 总赞数
@admin.route("/likes/numbers", methods=["POST"])
def likes_numbers():
    pass


# 注册用户量
@admin.route("/register/numbers", methods=["GET"])
@admin_login_required
def register_number():
    user = User.query.all()
    number = len(user)
    return jsonify(code=200, msg="查询成功", register_numbers=number)
