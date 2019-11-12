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
    username = db.Column(db.String(100), unique=True)  # 用户名　（唯一的）
    password = db.Column(db.String(100))  # 密码
    gender = db.Column(db.String(10), default=0)  # 性别
    avatar = db.Column(db.String(100))  # 照片路由
    info = db.Column(db.TEXT)  # 简介
    email = db.Column(db.String(100), unique=True)  # 邮箱（唯一的）
    degree = db.Column(db.Integer, default=0)  # 等级
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的最近上线时间

    my_articles = db.relationship('Blog', backref='user')  # 我的博客外键关系关联
    blog_col = db.relationship('CollectBlogArticle', backref='user')  # 博客收藏外键关系关联
    search_history = db.relationship('SearchHistory', backref='user')  # 搜索历史外键关系关联
    user_operate_log = db.relationship('UserOperateLog', backref='user')  # 用户操作日志关联
    user_login_log = db.relationship('UserLoginLog', backref='user')  # 用户登录日志关联

    """回复评论　私聊　关注　关系关联"""
    reply_sent = db.relationship('Comment', foreign_keys='Comment.sender_id',
                                 backref='author', lazy='dynamic')  # 我发的
    reply_received = db.relationship('Comment', foreign_keys='Comment.recipient_id',
                                     backref='recipient', lazy='dynamic')  # 我收的
    message_sent = db.relationship('Message', foreign_keys='Message.sender_id',
                                   backref='author', lazy='dynamic')  # 我发的
    message_received = db.relationship('Message', foreign_keys='Message.recipient_id',
                                       backref='recipient', lazy='dynamic')  # 我收的

    following = db.relationship('Follow',
                                foreign_keys='Follow.follower_id',
                                backref=db.backref('follower', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')  # 我关注的
    followers = db.relationship('Follow',
                                foreign_keys='Follow.followed_id',
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')  # 关注我的

    def __repr__(self):
        return "<User %r>" % self.username


# 博客信息
class Blog(db.Model):
    __tablename__ = "blog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.TEXT)  # 标题
    content = db.Column(db.TEXT)  # 内容
    summary = db.Column(db.TEXT)  # 简介
    logo = db.Column(db.String(200))  # 封面
    status = db.Column(db.Integer)  # 文章状态 1发表可见 2保存草稿不发表 3屏蔽不可见
    tag = db.relationship("Tag", backref="blog")  # 标签
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    comment = db.relationship('Comment', backref='blog')  # 评论外键关系关联
    page_view = db.Column(db.Integer, default=0)  # 浏览次数
    like_number = db.Column(db.Integer, default=0)  # 点赞次数
    comment_number = db.Column(db.Integer, default=0)  # 评论次数
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录更新时间

    def __repr__(self):
        return "<Blog %r>" % self.id


# 搜索历史
class SearchHistory(db.Model):
    __tablename__ = "search_history"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    keyword = db.Column(db.TEXT)  # 搜索内容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    add_time = db.Column(db.DateTime, default=datetime.now)  # 记录添加时间

    def __repr__(self):
        return "<SearchHistory %r>" % self.id


# 收藏文章
class CollectBlogArticle(db.Model):
    __tablename__ = "collect_blog_article"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客
    add_time = db.Column(db.DateTime, default=datetime.now)  # 记录添加时间

    def __repr__(self):
        return "<CollectBlogArticle %r>" % self.user_id


# 关注
class Follow(db.Model):
    __tablename__ = 'follow'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)  # 关注者
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)  # 被关注者
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Follow %r ---关注---> %r >" % self.follower_id, self.followed_id


# 私信
class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 发送者
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 发送者
    content = db.Column(db.TEXT)  # 内容
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Message %r ---关注---> %r >" % self.sender_id, self.recipient_id


# 评论博客
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    comment_id = db.Column(db.Integer)  # 评论对象编号id
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 发送者
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 接收者
    content = db.Column(db.TEXT)  # 回复内容
    type = db.Column(db.Integer)  # 类型，1是评论，2是回复
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))  # 所属博客文章
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id


# 用户登录日志
class UserLoginLog(db.Model):
    __tablename__ = "user_login_log"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    ip = db.Column(db.String(20))  # ip地址
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<UserLoginLog %r>" % self.user_id


# 用户操作日志
class UserOperateLog(db.Model):
    __tablename__ = "user_operate_log"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    ip = db.Column(db.String(20))  # ip地址
    detail = db.Column(db.String(250))  # 操作详情
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<UserOperateLog %r>" % self.user_id


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    username = db.Column(db.String(100), unique=True)  # 管理员用户名　（唯一的）
    password = db.Column(db.String(100))  # 管理员密码
    avatar = db.Column(db.String(100))  # 头像路由
    authority = db.Column(db.Integer)  # 权限等级
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的最近上线时间

    admin_operate_log = db.relationship('AdminOperateLog', backref='admin')  # 用户操作日志关联
    admin_login_log = db.relationship('AdminLoginLog', backref='admin')  # 用户登录日志关联
    board = db.relationship('Board', backref='admin')  # 公告牌关系关联

    def __repr__(self):
        return "<Admin %r>" % self.username


# 管理员登录日志
class AdminLoginLog(db.Model):
    __tablename__ = "admin_login_log"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(20))  # ip地址
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<AdminLoginLog %r>" % self.admin_id


# 管理员操作日志
class AdminOperateLog(db.Model):
    __tablename__ = "admin_operate_log"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(20))  # ip地址
    detail = db.Column(db.String(250))  # 操作详情
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<AdminOperateLog %r>" % self.admin_id


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"), nullable=False)  # 所属的文章编号
    name = db.Column(db.String(20))
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Tag %r>" % self.name


# 公告
class Board(db.Model):
    __tablename__ = "board"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.TEXT)  # 标题
    content = db.Column(db.TEXT)  # 内容
    add_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员

    def __repr__(self):
        return "<Board %r>" % self.title


if __name__ == '__main__':
    db.create_all()




