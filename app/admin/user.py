# -*- coding: utf-8 -*-
from .mixin import ModelViewMixin, BaseViewMixin
from flask import redirect, request, url_for, flash, views
from ..models import UserModel
from .. import app, db
from . import admin
from flask.ext.admin import expose_plugview
from datetime import datetime
from werkzeug import secure_filename
import os


labels = dict(
    id='#',
    user_name=u'用户名',
    nick_name=u'姓名',
    role=u'角色',
    date_created=u'创建时间'
)

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class UserAdmin(ModelViewMixin):
    column_labels = labels
    can_restore = False
    can_create = True
    can_edit = True
    can_delete = True

    column_searchable_list = ['user_name']
    column_list = ('id', 'user_name', 'nick_name', 'role', 'date_created')
    list_template = 'admin/user.html'

    def __init__(self, session, **kwargs):
        super(UserAdmin, self).__init__(UserModel, session, **kwargs)

    def scaffold_form(self):
        form_class = super(UserAdmin, self).scaffold_form()
        return form_class


class TeacherAdmin(BaseViewMixin):
    def is_visible(self):
        return False

    @expose_plugview('/')
    class ImportTeacher(views.MethodView):
        def post(self, cls):
            now = datetime.utcnow()
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = now.strftime('teachers_%Y-%m-%d(%H:%M:%s).xls')
                file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print file_url
                file.save(file_url)
            return redirect(url_for('admin.index'))


admin.add_view(
    UserAdmin(
        db.session, category=u'用户管理', name=u'用户列表', url='user'
    )
)
admin.add_view(TeacherAdmin(url='import_teacher'))
