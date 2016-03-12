# -*- coding: utf-8 -*-
from app import app, db
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms import widgets, fields  # noqa
from .user import UserModel
from .comptea import CompTea


competition_student = db.Table(
    'competition_student',
    db.Column('competition_id',
              db.Integer,
              db.ForeignKey('competition.id')),
    db.Column('student_id',
              db.Integer,
              db.ForeignKey('student.id'))
)
'''
competition_teacher = db.Table(
    'competition_teacher',
    db.Column('competition_id',
              db.Integer,
              db.ForeignKey('competition.id')),
    db.Column('teacher_id',
              db.Integer,
              db.ForeignKey('user.id'))
)
'''
'''竞赛项目'''


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(128), nullable=False)
    date_created = db.Column(
        db.TIMESTAMP, index=True,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return self.project_name

    def project_to_json(self):
        return {
            'project_id': self.id,
            'project_name': self.project_name
        }

'''参与者'''


class Participant(db.Model):
    __tablename__ = 'participant'
    id = db.Column(db.Integer, primary_key=True)
    id_competition = db.Column(db.Integer, db.ForeignKey('competition.id'))
    id_student = db.Column(db.Integer, db.ForeignKey('student.id'))
    locant = db.Column(db.Integer)
    date_created = db.Column(
        db.TIMESTAMP, index=True,
        server_default=db.func.current_timestamp()
    )

    def __init__(self, locant):
        self.locant = locant

    def __repr__(self):
        return self.student.student_name

'''指导老师'''


class Adviser(db.Model):

    __tablename__ = 'adviser'

    id = db.Column(db.Integer, primary_key=True)
    id_competition = db.Column(db.Integer, db.ForeignKey('competition.id'))
    id_teacher = db.Column(db.Integer, db.ForeignKey('user.id'))
    locant = db.Column(db.Integer)

    def __init__(self, locant):
        self.locant = locant

    def __repr__(self):
        return self.teacher.nick_name


'''竞赛信息'''


class Competition(db.Model):
    __tablename__ = 'competition'
    id = db.Column(db.Integer, primary_key=True)
    id_project = db.Column(db.Integer,
                           db.ForeignKey('project.id'))
    achievement_name = db.Column(db.String(128))
    awards_unit = db.Column(db.String(128))
    winning_time = db.Column(db.Date, nullable=False)
    is_review = db.Column(db.Boolean, default=False)
    date_created = db.Column(
        db.TIMESTAMP, index=True,
        server_default=db.func.current_timestamp()
    )
    project = db.relationship('Project', lazy=True)

    students = db.relationship('Student',
                               secondary=competition_student,
                               single_parent=True,
                               backref=db.backref(
                                   'competitions', lazy='joined'),
                               lazy='dynamic')
    '''
    teachers = db.relationship('UserModel',
                               secondary=competition_teacher,
                               single_parent=True,
                               backref=db.backref(
                                   'competitions', lazy='joined'),
                               lazy='dynamic')
    '''

    winning_level = db.Column(db.Enum(
        *app.config['COMPETITION_LEVEL'],
        name='competition_level_enum'))

    rate = db.Column(db.Enum(
        *app.config['COMPETITION_RATE'],
        name='competition_rate_enum'))

    teachers = db.relationship(
        'CompTea',
        foreign_keys=[CompTea.competition_id],
        backref=db.backref('competitions', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    @classmethod
    def model_form(cls, *args, **kwargs):
        return model_form(
            model=cls,
            db_session=db.session,
            field_args={
                'winning_level': {'widget': widgets.Select()},
                'rate': {'widget': widgets.Select()}
            }
        )

    def competition_to_json(self):
        return {
            'id': self.id,
            'achievement_name': self.achievement_name,
            'awards_unit': self.awards_unit,
            'winning_level': self.winning_level,
            'rate': self.rate,
            'project': self.project.project_to_json()
        }


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

    @classmethod
    def model_form(cls):
        return model_form(
            model=cls,
            db_session=db.session
        )

    def __repr__(self):
        return self.student_id + '/' + self.student_name
