from . import main
from app import db, redis_store
from app.models import User, Blog, UserOperateLog, Message, Comment, CollectBlogArticle
from flask import request, jsonify, current_app, session, g
from app.utils.tool import user_login_required


# 评论
@main.route("/comment", methods=["POST"])
@user_login_required
def comment():
    req_json = request.get_json()
    ip_addr = request.remote_addr
    sender_id = g.user_id
    blog_id = req_json.get("blog_id")
    content = req_json.get("content")
    if not all([sender_id, blog_id, content, ip_addr]):
        return jsonify(code=4000, msg="参数不完整")
    com = Comment(sender_id=sender_id, blog_id=blog_id, content=content)
    try:
        db.session.add(com)
        detail = "提交了评论"
        user_log = UserOperateLog(user_id=sender_id, ip=ip_addr, detail=detail)
        db.session.add(user_log)
        db.session.commit()
        return jsonify(code=200, msg="发布评论成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="操作数据库失败,请稍后再试")


# 删自己评论
@main.route("/comment", methods=["DELETE"])
@user_login_required
def delete_comment():
    req_json = request.get_json()
    ip_addr = request.remote_addr
    sender_id = g.user_id
    comment_id = req_json.get("comment_id")
    if not all([sender_id, comment_id, ip_addr]):
        return jsonify(code=4000, msg="参数不完整")

    try:
        # 删除评论
        blog = Comment.query.filter(Comment.id == comment_id, Comment.sender_id == sender_id).delete()
        if blog != 1:
            return jsonify(code=400, msg="删除评论失败，评论不存在或者你不是评论主人")
        detail = "删除了评论 %d " % comment_id
        user_log = UserOperateLog(user_id=sender_id, ip=ip_addr, detail=detail)
        db.session.add(user_log)
        db.session.commit()
        return jsonify(code=200, msg="删除了评论成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="删除评论失败，请稍后再试")


# 收藏博客
@main.route("/blog/collect", methods=["POST"])
@user_login_required
def blog_collect():
    req_json = request.get_json()
    ip_addr = request.remote_addr
    user_id = g.user_id
    blog_id = req_json.get("blog_id")
    if not all([user_id, blog_id, ip_addr]):
        return jsonify(code=4000, msg="参数不完整")

    blog = Blog.query.get(blog_id)
    if blog_id is None or blog.status != "正常":
        return jsonify(code=4001, msg="博客不存在")

    # 查询是否已经收藏
    try:
        bc_find = CollectBlogArticle.query.filter(CollectBlogArticle.user_id == user_id,
                                                  CollectBlogArticle.blog_id == blog_id).first()
        if bc_find is not None:
            return jsonify(code=4002, msg="你已经收藏")
    except Exception as e:
        print(e)
        return jsonify(code=400, msg="查询数据库失败,请稍后再试")

    # 添加收藏
    bc = CollectBlogArticle(user_id=user_id, blog_id=blog_id)
    try:
        db.session.add(bc)
        detail = "收藏了文章 %s" % blog_id
        user_log = UserOperateLog(user_id=user_id, ip=ip_addr, detail=detail)
        db.session.add(user_log)
        db.session.commit()
        return jsonify(code=200, msg="收藏文章成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="操作数据库失败,请稍后再试")


# 取消收藏博客
@main.route("/blog/collect", methods=["DELETE"])
@user_login_required
def delete_blog_collect():
    req_json = request.get_json()
    ip_addr = request.remote_addr
    user_id = g.user_id
    collect_blog_article_id = req_json.get("collect_blog_article_id")
    if not all([user_id, collect_blog_article_id, ip_addr]):
        return jsonify(code=4000, msg="参数不完整")

    try:
        # 取消收藏
        delete_collect_blog_article = CollectBlogArticle.query.filter(CollectBlogArticle.id == collect_blog_article_id,
                                                                      CollectBlogArticle.user_id == user_id).delete()
        if delete_collect_blog_article != 1:
            return jsonify(code=400, msg="取消收藏博客失败,查不到相关收藏信息")
        detail = "取消收藏博客 %d " % collect_blog_article_id
        user_log = UserOperateLog(user_id=user_id, ip=ip_addr, detail=detail)
        db.session.add(user_log)
        db.session.commit()
        return jsonify(code=200, msg="取消收藏博客成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="取消收藏博客失败，请稍后再试")


# 反馈
@main.route("/message", methods=["POST"])
@user_login_required
def message():
    req_json = request.get_json()
    ip_addr = request.remote_addr
    sender_id = g.user_id
    recipient_id = req_json.get("recipient_id")
    content = req_json.get("content")
    if not all([sender_id, recipient_id, content, ip_addr]):
        return jsonify(code=4000, msg="参数不完整")
    msg = Message(sender_id=sender_id, recipient_id=recipient_id, content=content)
    try:
        db.session.add(msg)
        detail = "提交了反馈留言"
        user_log = UserOperateLog(user_id=sender_id, ip=ip_addr, detail=detail)
        db.session.add(user_log)
        db.session.commit()
        return jsonify(code=200, msg="你的反馈发送成功,感谢你的反馈")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="操作数据库失败,请稍后再试")


# 搜索
@main.route("/blog/search/<int:page>", methods=["POST"])
def blog_search(page):
    keyword = request.get_json().get("keyword")
    if not page:
        page = 1
    else:
        page = int(page)

    if keyword is None:
        return jsonify(code=400, msg="请输入搜索内容"), 400

    key_remark = keyword
    blogs = Blog.query.filter_by(status="正常").filter(Blog.title.like("%" + key_remark + "%")).paginate(page,
                                                                                                       per_page=5,
                                                                                                       error_out=False).items
    payload = [blog.to_dict() for blog in blogs]
    return jsonify(code=200, msg="搜索结束", data=payload)


# 获取博客详情
@main.route("/blog/article/detail/<int:blog_id>", methods=["GET", "POST"])
def get_article_detail(blog_id):
    blog = Blog.query.get(blog_id)
    if blog is None or blog.status != "正常":
        return jsonify(code=4001, msg="博客不存在")
    try:
        # 增加浏览次数
        blog.page_views += 1
        db.session.add(blog)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

    try:
        data = blog.to_dict()

        return jsonify(code=200, data=data)
    except Exception as e:
        print(e)
        return jsonify(code=4002, msg="出错")
