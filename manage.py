# -*- coding: utf-8 -*-
from app import app, db
from app.models import UserModel, RoleModel
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand, upgrade

manager = Manager(app)


def make_shell_context():
    return dict(
        app=app,
        db=db,
        UserModel=UserModel,
        RoleModel=RoleModel
    )

manager.add_command("runserver", Server(host="0.0.0.0", port="3000"))
manager.add_command("shell", Shell(make_context=make_shell_context))

migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)


@manager.command
def deploy():
    db.drop_all()
    db.create_all()

    try:
        RoleModel.insert_roles()
        r = RoleModel.query.filter_by(role_name='管理员').first()
        u = UserModel()
        u.user_name = 'admin'
        u.nick_name = 'admin'
        u.password = 'admin'
        u.role = r
        db.session.add(u)
        db.session.commit()
    except Exception, e:
        print e
        db.session.rollback()

if __name__ == '__main__':
    manager.run()
