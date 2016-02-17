# -*- coding: utf-8 -*-
from .mixin import ModelViewMixin
from flask import redirect, url_for, request
from ..models import PatentModel
from .. import app, db
from . import admin


class PatentAdmin(ModelViewMixin):
    column_list = [
        'id',
        'category',
        'student_name',
        'student_class',
        'precedence',
        'teacher_name',
        'patent_number',
        'certificate',
        'public',
        'acachemy'
    ]

    labels = dict(
        id=u'序号',
        category=u'专利类别',
        student_name=u'学生姓名',
        student_class=u'班级',
        precedence=u'位次',
        teacher_name=u'指导教师',
        patent_number=u'专利号',
        certificate=u'证书号',
        public=u'授权时间',
        acachemy=u'学院'
    )

    column_labels = labels

    def __init__(self, session, **kwargs):
        super(PatentAdmin, self).__init__(PatentModel, session, **kwargs)

    def scaffold_form(self):
        form_class = super(PatentAdmin, self).scaffold_form()
        return form_class

admin.add_view(
    PatentAdmin(
        db.session, name=u'专利管理', url='patent'
    )
)
