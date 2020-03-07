from . import main
from app import db, redis_store
from app.models import User, Blog, UserOperateLog, Message
from flask import request, jsonify, current_app, session, g
from app.utils.tool import user_login_required


# 评论
@main.route("/comment", methods=["POST"])
def comment():
    pass


# 删自己评论
@main.route("/comment", methods=["POST"])
def delete_comment():
    pass


# 收藏博客
@main.route("/blog/collect", methods=["POST"])
def blog_collect():
    pass


# 取消收藏博客
@main.route("/blog/collect", methods=["DELETE"])
def delete_blog_collect():
    pass


# 点赞
@main.route("/like", methods=["POST"])
def make_like():
    pass


# 取消点赞
@main.route("/dislike", methods=["POST"])
def make_unlike():
    pass


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
@main.route("/blog/search", methods=["POST"])
def blog_search():
    pass


# 获取博客详情
@main.route("/blog/article/detail", methods=["GET"])
def get_article_detail():
    pass
