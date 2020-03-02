from . import main
from app import db, redis_store
from app.models import User, Blog, UserOperateLog
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
def message():
    pass


# 搜索
@main.route("/blog/search", methods=["POST"])
def blog_search():
    pass




