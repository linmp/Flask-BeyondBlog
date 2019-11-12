from . import main
from app import db, redis_store
from app.models import User, Blog


# 加好友
@main.route("/friend", methods=["POST"])
def add_friend():
    pass


# 删好友
@main.route("/friend", methods=["DELETE"])
def delete_friend():
    pass


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


# 关注博主
@main.route("/follow", methods=["POST"])
def follow():
    pass


# 取消删除博主
@main.route("/follow", methods=["DELETE"])
def unfollow():
    pass


# 点赞
@main.route("/like", methods=["POST"])
def make_like():
    pass


# 取消点赞
@main.route("/unlike", methods=["POST"])
def make_unlike():
    pass


# 私信
@main.route("/message", methods=["POST"])
def message():
    pass


# 获取个人信息
@main.route("/profile", methods=["POST"])
def get_profile():
    pass


# 修改个人信息
@main.route("/profile", methods=["POST"])
def change_profile():
    pass


# 搜索
@main.route("/blog/search", methods=["POST"])
def blog_search():
    pass


# 找回密码
@main.route("/password", methods=["POST"])
def find_password():
    pass


# 更新密码
@main.route("/password", methods=["PUT"])
def change_password():
    pass
