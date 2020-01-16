from . import admin
from app.models import AdminLoginLog, AdminOperateLog
from flask import g
from app.utils.tool import admin_login_required
import json


# 获取登录日志
@admin.route("/login/log", methods=["GET"])
@admin_login_required
def login_log():
    """
    等待优化---> 加入缓存
    :return:
    """
    admin_id = g.admin_id
    # admin_login_logs = AdminLoginLog.query.filter_by(admin_id=admin_id).all() # 修改了按照时间倒序
    admin_login_logs = AdminLoginLog.query.filter_by(admin_id=admin_id).order_by(AdminLoginLog.add_time.desc())
    admin_log_li = []
    for admin_login_log in admin_login_logs:
        admin_log_li.append(admin_login_log.to_dict())

    # 将数据转换为json字符串
    resp_dict = dict(re_code=200, msg="管理员登录日志", data=admin_log_li)
    resp_json = json.dumps(resp_dict)
    return resp_json, 200, {"Content-Type": "application/json"}


# 获取操作日志
@admin.route("/operate/log", methods=["GET"])
@admin_login_required
def operate_log():
    admin_id = g.admin_id
    # admin_operate_logs = AdminOperateLog.query.filter_by(admin_id=admin_id).all()
    admin_operate_logs = AdminOperateLog.query.filter_by(admin_id=admin_id).order_by(AdminOperateLog.add_time.desc())
    admin_operate_log_li = []
    for admin_operate_log in admin_operate_logs:
        admin_operate_log_li.append(admin_operate_log.to_dict())

    # 将数据转换为json字符串
    resp_dict = dict(re_code=200, msg="管理员操作日志", data=admin_operate_log_li)
    resp_json = json.dumps(resp_dict)
    return resp_json, 200, {"Content-Type": "application/json"}
