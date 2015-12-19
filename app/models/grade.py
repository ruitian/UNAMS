# -*- coding: UTF-8 -*-
from app import db


class Grade(db.Model):

    '''年级信息表，字段包括：
    年级编号，年级名称'''

    __tablename__ = 'grade'
    id = db.Column(db.Integer, primary_key=True)
    grade_name = db.Column(db.String(128), nullable=False, unique=True)
    date_created = db.Column(
        db.TIMESTAMP, index=True,
        server_default=db.func.current_timestamp()
    )

    students = db.relationship('Student', backref='grade', lazy='dynamic')

    def __repr__(self):
        return self.grade_name
