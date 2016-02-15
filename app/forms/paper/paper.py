# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import SubmitField, StringField, DateTimeField
from wtforms.validators import Required


class PaperForm(Form):
    paper_title = StringField(u'论文题目', validators=[Required()])
    issn = StringField(u'刊号', validators=[Required()])
    precedence = StringField(u'位次', validators=[Required()])
    periodical = StringField(u'刊物名称', validators=[Required()])
    public = StringField(u'发表时间', validators=[Required()])
    student_name = StringField(u'作者', validators=[Required()])
    acachemy = StringField(u'学院', validators=[Required()])
    grade = StringField(u'班级', validators=[Required()])
    level = StringField(u'档次', validators=[Required()])
    submit = SubmitField(u'提交信息')
