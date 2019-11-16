from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app("develop")
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)


# 初始化管理员账号数据,添加manager命令
@manager.command
def create_admin():
    from app.models import Admin
    from config_message.constant import ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_AVATAR_URL, ADMIN_POWER
    try:
        admin_new = Admin(username=ADMIN_USERNAME, password=ADMIN_PASSWORD, avatar=ADMIN_AVATAR_URL,
                          authority=ADMIN_POWER)
        db.session.add(admin_new)
        db.session.commit()
        print("初始化成功")
    except:
        print("初始化失败")
        db.session.rollback()


if __name__ == '__main__':
    manager.run()
