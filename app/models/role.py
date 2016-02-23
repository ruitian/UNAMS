# -*- coding: utf-8 -*-
from app import db


class RoleModel(db.Model):

    '''角色表'''

    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('UserModel', backref='role', lazy='dynamic')

    def __repr__(self):
        return self.role_name

    def __init__(self, role_name):
        self.role_name = role_name

    @staticmethod
    def insert_roles():
        roles = {
            u'教师': (0x04),
            u'单位管理员': (0x08),
            u'管理员': (0x80)
        }
        for r in roles:
            role = RoleModel.query.filter_by(role_name=r).first()
            if role is None:
                role = RoleModel(role_name=r)
                role.permissions = roles[r]
                db.session.add(role)
        db.session.commit()
