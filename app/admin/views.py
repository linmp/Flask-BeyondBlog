from . import admin
from app import db
from app.utils.tool import admin_login_required
from app.models import Board, AdminOperateLog
from flask import g, request, jsonify, session


# 新增标签
@admin.route("/tag", methods=["POST"])
def add_tag():
    pass


# 删除标签
@admin.route("/tag", methods=["POST"])
def delete_tag():
    pass


# 新增管理员
@admin.route("/manager", methods=["POST"])
def add_manager():
    pass


# 删除管理员
@admin.route("/manager", methods=["DELETE"])
def delete_manager():
    pass


# 删除博客
@admin.route("/blog", methods=["DELETE"])
def delete_blog():
    pass


# 屏蔽用户
@admin.route("/user/status", methods=["POST"])
def delete_user():
    pass


# 删除评论
@admin.route("/comment", methods=["DELETE"])
def delete_comment():
    pass


# 更改背景
@admin.route("/background", methods=["DELETE"])
def change_background():
    pass


# 发送公告
@admin.route("/bulletin/board", methods=["POST"])
@admin_login_required
def bulletin_board():
    admin_id = g.admin_id  # 获取管理员的id
    admin_name = session.get("username")  # 获取管理员的名字
    ip_addr = request.remote_addr  # 获取管理员登录的ip
    req_dict = request.get_json()
    title = req_dict.get("title")
    content = req_dict.get("content")

    # 校验参数
    # 参数完整的校验
    if not all([title, content, ip_addr]):
        return jsonify(re_code=400, msg="参数不完整")

    # 将数据保存
    board = Board(title=title, content=content, admin_id=admin_id)

    try:
        detail = "管理员 用户名:%s  id:%s  新发送了公告 <%s> " % (admin_name, admin_id, title)
        admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
        db.session.add(board)
        db.session.add(admin_operate_log)
        db.session.commit()
        return jsonify(re_code=200, msg="保存数据成功")
    except:
        db.session.rollback()
        return jsonify(re_code=400, msg="保存数据失败")


# 私信博主
@admin.route("/message", methods=["POST"])
def message():
    pass


# 统计浏览量
@admin.route("views/numbers", methods=["POST"])
def views_numbers_count():
    pass


# 任务板
@admin.route("task", methods=["POST"])
def task_board():
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
@admin.route("/register/numbers", methods=["POST"])
def register_number():
    pass
