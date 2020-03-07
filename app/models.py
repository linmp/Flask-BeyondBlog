from . import db
from datetime import datetime

"""
python3 manage.py db init
python3 manage.py db migrate -m "message"
python3 manage.py db upgrade
python3 manage.py db downgrade
"""


# 用户信息
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    username = db.Column(db.String(128), unique=True)  # 用户名　（唯一的）
    password = db.Column(db.String(128))  # 密码
    avatar = db.Column(db.String(256))  # 照片路由
    phone = db.Column(db.String(11))  # 手机号
    status = db.Column(db.Enum("正常", "删除"), default="正常", nullable=False)  # 用户的状态
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的最近上线时间

    blog_col = db.relationship('CollectBlogArticle', backref='user')  # 博客收藏外键关系关联
    search_history = db.relationship('SearchHistory', backref='user')  # 搜索历史外键关系关联
    user_operate_log = db.relationship('UserOperateLog', backref='user')  # 用户操作日志关联
    user_login_log = db.relationship('UserLoginLog', backref='user')  # 用户登录日志关联
    reply_sent = db.relationship('Comment', foreign_keys='Comment.sender_id',
                                 backref='sender', lazy='dynamic')  # 我发的评论

    message_sent = db.relationship('Message', foreign_keys='Message.sender_id',
                                   backref='sender')  # 我发的反馈

    def __repr__(self):
        return "<User %r>" % self.username

    def to_dict(self):
        """将对象转换为字典数据"""
        user_dict = {
            "user_id": self.id,
            "username": self.username,
            "avatar": self.avatar,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return user_dict

    def is_normal(self):
        """
        判断用户是否能用
        :return:
        """
        if self.status == "正常":
            return True
        else:
            return False


# 搜索历史
class SearchHistory(db.Model):
    __tablename__ = "search_history"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    keyword = db.Column(db.TEXT)  # 搜索内容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录添加时间

    def __repr__(self):
        return "<SearchHistory %r>" % self.id


# 收藏文章
class CollectBlogArticle(db.Model):
    __tablename__ = "collect_blog_article"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录添加时间

    def __repr__(self):
        return "<CollectBlogArticle %r>" % self.user_id


# 反馈
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 发送者
    recipient_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 接收者
    content = db.Column(db.Text)  # 内容
    create_time = db.Column(db.DateTime, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Message %r to %r >" % self.sender_id, self.recipient_id


# 评论博客
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 发送者
    content = db.Column(db.Text)  # 评论内容
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客文章
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id


# 用户登录日志
class UserLoginLog(db.Model):
    __tablename__ = "user_login_log"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    ip = db.Column(db.String(128))  # ip地址
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<UserLoginLog %r>" % self.user_id


# 用户操作日志
class UserOperateLog(db.Model):
    __tablename__ = "user_operate_log"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    ip = db.Column(db.String(128))  # ip地址
    detail = db.Column(db.String(256))  # 操作详情
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<UserOperateLog %r>" % self.user_id


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    username = db.Column(db.String(128), unique=True)  # 管理员用户名　（唯一的）
    password = db.Column(db.String(128))  # 管理员密码
    avatar = db.Column(db.String(256))  # 头像路由
    power = db.Column(db.Enum("超级管理员", "管理员"))  # 权限等级 只有超级管理员能创建用户
    status = db.Column(db.Enum("正常", "删除"), default="正常", nullable=False)  # 管理员的状态
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的最近上线时间

    my_articles = db.relationship('Blog', backref='admin')  # 我的博客外键关系关联
    admin_operate_logs = db.relationship('AdminOperateLog', backref='admin')  # 操作日志关联
    admin_login_logs = db.relationship('AdminLoginLog', backref='admin')  # 登录日志关联
    boards = db.relationship('Board', backref='admin')  # 公告牌关系关联
    message_gets = db.relationship('Message', backref='admin')  # 收到的

    def __repr__(self):
        return "<Admin %r>" % self.username


# 博客信息
class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.TEXT)  # 标题
    content = db.Column(db.TEXT)  # 内容
    summary = db.Column(db.TEXT)  # 简介
    logo = db.Column(db.String(256))  # 封面
    status = db.Column(db.Enum("正常", "草稿", "删除"), default="正常", nullable=False)  # 文章状态
    author_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属博主

    tags = db.relationship("Tag", secondary="blog_to_tag", backref="blog")  # 标签关系关联
    blog_followers = db.relationship('CollectBlogArticle', backref='blog')  # 被收藏外键关系关联
    comments = db.relationship('Comment', backref='blog')  # 评论外键关系关联
    page_views = db.Column(db.Integer, default=0)  # 浏览次数
    like_numbers = db.Column(db.Integer, default=0)  # 点赞次数
    comment_numbers = db.Column(db.Integer, default=0)  # 评论数
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录更新时间

    def __repr__(self):
        return "<Blog %r>" % self.id


# 博客 标签第三表
class BlogAndTag(db.Model):
    __tablename__ = "blog_to_tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"), nullable=False)  # 所属的文章编号
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable=False)  # 所属的tag


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(32), nullable=False, unique=True)  # 标签名字
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Tag %r>" % self.name


# 公告
class Board(db.Model):
    __tablename__ = "board"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.Text)  # 标题
    content = db.Column(db.Text)  # 内容
    status = db.Column(db.Enum("正常", "删除"))  # 状态
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员

    def __repr__(self):
        return "<Board %r>" % self.title


# 管理员登录日志
class AdminLoginLog(db.Model):
    __tablename__ = "admin_login_log"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(128))  # ip地址
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<AdminLoginLog %r>" % self.admin_id

    def to_dict(self):
        """将对象转换为字典数据"""
        login_log_dict = {
            "admin_id": self.admin_id,
            "ip": self.ip,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return login_log_dict


# 管理员操作日志
class AdminOperateLog(db.Model):
    __tablename__ = "admin_operate_log"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(128))  # ip地址
    detail = db.Column(db.String(256))  # 操作详情
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<AdminOperateLog %r>" % self.admin_id

    def to_dict(self):
        """将对象转换为字典数据"""
        operate_log_dict = {
            "id": self.id,
            "admin_id": self.admin_id,
            "ip": self.ip,
            "detail": self.detail,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return operate_log_dict


if __name__ == '__main__':
    db.create_all()
