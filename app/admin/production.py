# -*- coding: utf-8 -*-
from .mixin import ModelViewMixin
from flask import redirect, url_for, request
from ..models import ProductionModel
from .. import app, db
from . import admin


class ProductionAdmin(ModelViewMixin):
    column_list = [
        'id',
        'pro_title',
        'pro_type',
        'pro_match',
        'pro_actor',
        'pro_time'
    ]

    labels = dict(
        id=u'序号',
        pro_title=u'作品名称',
        pro_type=u'作品类型',
        pro_match=u'参加比赛',
        pro_actor=u'设计者',
        pro_time=u'设计时间'
    )

    column_labels = labels

    def __init__(self, session, **kwargs):
        super(ProductionAdmin, self).__init__(
            ProductionModel, session, **kwargs)

    def scaffold_form(self):
        form_class = super(ProductionAdmin, self).scaffold_form()
        return form_class

admin.add_view(
    ProductionAdmin(
        db.session, name=u'作品管理', url='production'
    )
)
