# -*- coding: UTF-8 -*-
from .competition import Participant
from app import db
from wtforms.ext.sqlalchemy.orm import model_form


class Student(db.Model):

    '''学生信息表，字段包括：
    学生ID，学生姓名，学生所在学院，学生专业，学生所在年级'''

    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(128), nullable=False, unique=True)
    student_name = db.Column(db.String(128), nullable=False)

    id_grade = db.Column(db.Integer, db.ForeignKey('grade.id'))
    id_acachemy = db.Column(db.Integer, db.ForeignKey('unit.id'))
    id_major = db.Column(db.Integer, db.ForeignKey('major.id'))

    competitions = db.relationship(
        'Participant',
        foreign_keys=[Participant.id_student],
        backref=db.backref('student', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    @classmethod
    def model_form(cls):
        return model_form(
            model=cls,
            db_session=db.session
        )

    def __repr__(self):
        return self.student_id + '/' + self.student_name
