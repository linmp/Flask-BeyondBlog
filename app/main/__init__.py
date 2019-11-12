from flask import Blueprint

# 创建蓝图对象
main = Blueprint("main", __name__)
from . import views, authentic, blog
