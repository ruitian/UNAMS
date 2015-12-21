# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Length


class StudentForm(Form):
    student_id = StringField(u'学号', validators=[Required()])
    student_name = StringField(u'学生姓名', validators=[Required()])
    id_grade = StringField(u'所在年级', validators=[Required()])
    id_acachemy = StringField(u'所在学院')
    id_major = StringField(u'专业')
    submit = SubmitField(u'确认添加')
