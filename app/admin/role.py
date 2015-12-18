# -*- coding: utf-8 -*-
from .mixin import ModelViewMixin
from flask import redirect, url_for, request
from ..models import RoleModel
from .. import app, db
from . import admin


class RoleAdmin(ModelViewMixin):
    column_list = ['role_name']

    def __init__(self, session, **kwargs):
        super(RoleAdmin, self).__init__(RoleModel, session, **kwargs)

    def scaffold_form(self):
        form_class = super(RoleAdmin, self).scaffold_form()
        return form_class

admin.add_view(
    RoleAdmin(
        db.session, category=u'用户管理', name=u'角色列表', url='role'
    )
)
