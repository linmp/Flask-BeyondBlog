from . import main
from app import db, redis_store
from app.models import User, Blog, Follow, UserOperateLog
from flask import request, jsonify, current_app, session, g
from app.utils.tool import user_login_required


# 加好友
@main.route("/friend", methods=["POST"])
@user_login_required
def add_friend():
    """
    添加好友
    输入对方的user_id
    然后系统发信息通知对方同意
    如果两个都是对方好友 则可以私信
    否则 不行
    :return:
    """
    pass


# 删好友
@main.route("/friend", methods=["DELETE"])
def delete_friend():
    """
    输入对方user_id 进行删除
    :return:
    """
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
@main.route("/user/follow", methods=["POST"])
@user_login_required
def follow():
    req_json = request.get_json()
    following_user_id = req_json.get("user_id")
    my_user_id = g.get("user_id")
    my_username = session.get("username")

    if not following_user_id:
        return jsonify(re_code=400, msg="参数不完整")

    try:
        user = User.query.get(following_user_id)
    except Exception as e:
        current_app.logger.error(e)
        user = None
    if not user:
        return jsonify(re_code=400, msg="查询不到当前要关注的用户")

    try:
        ip_addr = request.remote_addr  # 获取用户的ip
        operate_detail = "用户id:%r,用户名:%s,关注了id:%r,用户名:%s" % (my_user_id, my_username, user.id, user.username)
        user_operate_log = UserOperateLog(user_id=user.id, ip=ip_addr, detail=operate_detail)
        try_follow = Follow(follower_id=my_user_id, followed_id=following_user_id)
        db.session.add(user_operate_log)
        db.session.add(try_follow)
        db.session.commit()
        return jsonify(re_code=200, msg="关注用户成功 !")
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(re_code=400, msg="数据库失败,关注用户失败,请稍后重试")
    # 添加用户操作日志


# 取消删除博主
@main.route("/user/follow", methods=["DELETE"])
@user_login_required
def un_follow():
    """
    先查询是否已经有关注表
    如关注了就删除
    :return:
    """
    req_json = request.get_json()
    following_user_id = req_json.get("user_id")
    my_user_id = g.get("user_id")
    my_username = session.get("username")

    if not following_user_id:
        return jsonify(re_code=400, msg="参数不完整")

    find_follow = Follow.query.filter_by(follower_id=my_user_id, followed_id=following_user_id).first()

    if not find_follow:
        return jsonify(re_code=400, msg="还未关注对方!")

    following_user = User.query.get(following_user_id)
    if not following_user:
        return jsonify(re_code=400, msg="查询不到当前用户")

    try:
        ip_addr = request.remote_addr  # 获取用户的ip
        operate_detail = "用户id:%r,用户名:%s,取消关注了id:%r,用户名:%s" % (
        my_user_id, my_username, following_user.id, following_user.username)
        user_operate_log = UserOperateLog(user_id=my_user_id, ip=ip_addr, detail=operate_detail)
        db.session.add(user_operate_log)
        db.session.delete(find_follow)
        db.session.commit()
        return jsonify(re_code=200, msg="取消关注用户成功!")
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(re_code=400, msg="数据库失败,取消关注用户失败,请稍后重试")


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


# 搜索
@main.route("/blog/search", methods=["POST"])
def blog_search():
    pass
