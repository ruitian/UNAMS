# -*- coding: utf-8 -*-
from flask.ext.admin import Admin, AdminIndexView as _AdminIndexView
from flask.ext.login import current_user
from flask import redirect, url_for, request


class AdminIndexView(_AdminIndexView):
    def is_accessible(self):
        return (current_user.is_authenticated()
                and current_user.is_administrator())

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('login', next=request.url))

admin = Admin(name=u'大学生创新活动管理系统',
              index_view=AdminIndexView(name=u'首页'),
              base_template='admin/base.html',
              template_mode='admin')
from . import user  # noqa
from . import role  # noqa
from . import department  # noqa
from . import competition  # noqa
from . import paper  # noqa
from . import patent  # noqa
