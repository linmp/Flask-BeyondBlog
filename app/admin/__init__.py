from flask import Blueprint

# 创建蓝图对象
main = Blueprint("admin", __name__)
from . import views