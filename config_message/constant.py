# 默认配置信息
import os

# 默认的管理员 账号和密码还有头像
ADMIN_USERNAME = "admin_beyond_lam"
ADMIN_PASSWORD = "admin_password"
ADMIN_AVATAR_URL = "https://images.pexels.com/photos/3031397/pexels-photo-3031397.jpeg"

# Mysql数据库信息配置
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'whatever-guess'
WTF_CSRF_ENABLED = False

# Redis配置信息
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = 6379

# flask-session配置
PERMANENT_SESSION_LIFETIME = 86400  # 86400 session数据的有效期，单位秒
