# 需要的配置
import os
import redis
from config_message.constant import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY, \
    WTF_CSRF_ENABLED, REDIS_HOST, REDIS_PORT, PERMANENT_SESSION_LIFETIME


class Config(object):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = SQLALCHEMY_TRACK_MODIFICATIONS
    SECRET_KEY = SECRET_KEY
    WTF_CSRF_ENABLED = WTF_CSRF_ENABLED

    # redis
    REDIS_HOST = REDIS_HOST
    REDIS_PORT = REDIS_PORT

    # flask-session配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理
    PERMANENT_SESSION_LIFETIME = PERMANENT_SESSION_LIFETIME  # session数据的有效期，单位秒


class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置信息"""
    pass


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}
