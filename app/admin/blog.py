from . import admin
from ..models import Blog, Admin, AdminOperateLog, Tag, db
from app.utils.tool import admin_login_required
from flask import request, jsonify, g


# 发表博客
@admin.route("/blog/article", methods=["POST"])
@admin_login_required
def post_blog_article():
    """
    title
    content
    summary
    admin_id
    tags = []
    :return: 
    """
    admin_id = g.admin_id  # 博主的id
    req_data = request.get_json()
    ip_addr = request.remote_addr
    title = req_data.get("title")  # 标题
    content = req_data.get("content")  # 内容
    summary = req_data.get("summary")  # 简介
    status = req_data.get("status")  # 状态 "正常", "草稿"

    tags = req_data.get("tags")  # ["name","name"]

    if not all([title, content, summary, tags]):
        return jsonify(code=4000, msg="参数不完整")

    if status not in ("正常", "草稿"):
        return jsonify(code=4001, msg="参数出错")

    try:
        blog = Blog(title=title, content=content, summary=summary, author_id=admin_id, status=status)
        # 查询标签添加博客标签
        t = Tag.query.filter(Tag.name.in_(tags)).all()
        blog.tags = t
        if status == "草稿":
            detail = "添加草稿: %s " % title
        else:
            detail = "发布博客: %s " % title
        admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
        db.session.add(blog)
        db.session.add(admin_operate_log)
        db.session.commit()

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=4002, msg="操作出错,数据库出错")

    return jsonify(code=200, msg="操作成功", id=blog.id)


# 修改博客状态
@admin.route("/blog/article/status", methods=["POST"])
@admin_login_required
def delete_blog_article():
    """
    status
    状态 正常 草稿
    :return:
    """
    req_data = request.get_json()
    ip_addr = request.remote_addr
    status = req_data.get("status")  # 博客状态 "正常", "草稿", "删除"
    bid = req_data.get("id")  # 博客id
    admin_id = g.admin_id  # 博主id

    if not all([ip_addr, status, bid, admin_id]):
        return jsonify(code=4000, msg="参数不完整")

    if status not in ["正常", "草稿", "删除"]:
        return jsonify(code=4001, msg="状态更改失败")

    blog = Blog.query.get(bid)
    if blog is None or blog.status == "删除":
        return jsonify(code=4002, msg="博客不存在")

    # 如果 不是超级管理员 也不是作者 那么出错
    if blog.author_id != admin_id and admin_id != 1:
        return jsonify(code=4002, msg="你不是作者")

    if blog.status == status:
        return jsonify(code=200, msg="操作成功")

    detail = "修改了文章状态: %s --> %s " % (blog.status, status)
    try:
        blog.status = status
        # 添加操作日志
        admin_operate_log = AdminOperateLog(admin_id=admin_id, ip=ip_addr, detail=detail)
        db.session.add(admin_operate_log)

        db.session.add(blog)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=4003, msg="修改出错,请稍后再试")

    return jsonify(code=200, msg="操作成功")
