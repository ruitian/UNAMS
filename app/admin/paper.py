# -*- coding: utf-8 -*-
from .mixin import ModelViewMixin
from flask import redirect, url_for, request
from ..models import PaperModel
from .. import app, db
from . import admin


class PaperAdmin(ModelViewMixin):
    column_list = [
        'student_name',
        'acachemy',
        'student_class',
        'paper_title',
        'periodical',
        'issn',
        'public',
        'level',
        'precedence'
    ]

    labels = dict(
        id=u'序号',
        paper_title=u'论文题目',
        periodical=u'刊物名称',
        issn=u'刊号',
        student_class=u'班级',
        student_name=u'作者',
        level=u'论文级别',
        precedence=u'位次',
        public=u'发表时间',
        acachemy=u'所属学院'
    )

    column_labels = labels

    def __init__(self, session, **kwargs):
        super(PaperAdmin, self).__init__(PaperModel, session, **kwargs)

    def scaffold_form(self):
        form_class = super(PaperAdmin, self).scaffold_form()
        return form_class

admin.add_view(
    PaperAdmin(
        db.session, name=u'论文管理', url='paper'
    )
)
