# -*- coding: utf-8 -*-
from .mixin import ModelViewMixin
from flask import redirect, url_for, request
from ..models import PatentModel
from .. import app, db
from . import admin


class PatentAdmin(ModelViewMixin):
    column_list = [
        'id'
    ]

    labels = dict(
        id=u'序号',
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
