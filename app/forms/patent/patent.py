# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import SubmitField, StringField, DateTimeField
from wtforms.validators import Required


class PatentForm(Form):
    patent_title = StringField(u'专利名称', validators=[Required()])
    category = StringField(u'专利类别', validators=[Required()])
    student_name = StringField(u'学生姓名', validators=[Required()])
    student_class = StringField(u'班级', validators=[Required()])
    precedence = StringField(u'位次', validators=[Required()])
    teacher_name = StringField(u'指导教师', validators=[Required()])
    patent_number = StringField(u'专利号', validators=[Required()])
    certificate = StringField(u'证书号', validators=[Required()])
    public = StringField(u'授权时间', validators=[Required()])
    acachemy = StringField(u'学院', validators=[Required()])
    submit = SubmitField(u'提交信息')
