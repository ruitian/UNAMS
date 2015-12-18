# -*- coding: utf-8 -*-
from app import db

'''
单位/学院信息
'''


class UnitModel(db.Model):
    __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(128))
    unit_id = db.Column(db.Integer)
    date_created = db.Column(
        db.TIMESTAMP, index=True,
        server_default=db.func.current_timestamp()
    )
    teachers = db.relationship('UserModel', backref='unit', lazy='dynamic')
    major = db.relationship('MajorModel', backref='unit', lazy='dynamic')

    def __repr__(self):
        return self.unit_name


class MajorModel(db.Model):
    __tablename__ = 'major'
    id = db.Column(db.Integer, primary_key=True)
    major_name = db.Column(db.String(128))
    major_id = db.Column(db.Integer)
    date_created = db.Column(
        db.TIMESTAMP, index=True,
        server_default=db.func.current_timestamp()
    )
    id_unit = db.Column(db.Integer, db.ForeignKey('unit.id'))
