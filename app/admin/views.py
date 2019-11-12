from . import admin


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
def bulletin_board():
    pass


# 私信博主
@admin.route("/message", methods=["POST"])
def message():
    pass


# 统计浏览量
@admin.route("views/numbers", methods=["POST"])
def views_numbers_count():
    pass


# 获取登录日志
@admin.route("/login/log", methods=["GET"])
def login_log():
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
