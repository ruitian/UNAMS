# -*- coding: utf-8 -*-
from .mixin import ModelViewMixin, BaseViewMixin
from flask import redirect, request, url_for, flash, views
from ..models import UserModel, RoleModel, UnitModel
from .. import app, db
from . import admin
from flask.ext.admin import expose_plugview
from datetime import datetime
from werkzeug import secure_filename
import os
import xlrd


labels = dict(
    id='#',
    user_name=u'用户名',
    nick_name=u'姓名',
    role=u'角色',
    unit=u'单位',
    date_created=u'创建时间'
)

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
    column_editable_list = ['nick_name']
    column_list = ('id', 'user_name',
                   'nick_name', 'unit', 'role', 'date_created')
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
                filename = now.strftime('teachers%Y%m%d.xls')
                file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print file_url
                file.save(file_url)
                bk = xlrd.open_workbook(file_url)
                shxrange = range(bk.nsheets)
                sh = bk.sheet_by_name("Sheet1")
                row_list = []
                for i in range(1, sh.nrows):
                    row_data = sh.row_values(i)
                    row_list.append(row_data)
                for item in row_list:
                    try:
                        teacher_id = item[0].encode('utf-8')
                        teacher_name = item[1].encode('utf-8')
                        unit_id = item[2].encode('utf-8')
                        unit_name = item[3].encode('utf-8')
                    except:
                        flash(u'更新数据失败，错误数据为%行' % i)
                        db.rollback
                    teacher = UserModel.query.filter_by(
                        user_name=teacher_id, nick_name=teacher_name).first()
                    unit = UnitModel.query.filter_by(
                        unit_id=unit_id).first()

                    if not unit:
                        unit = UnitModel()
                        unit.unit_id = unit_id
                        unit.unit_name = unit_name
                        db.session.add(unit)
                    if not teacher:
                        teacher = UserModel()
                        teacher.user_name = teacher_id
                        teacher.nick_name = teacher_name
                        teacher.role = \
                            RoleModel.query.filter_by(role_name=u'教师').first()
                        teacher.password = app.config['DEFAULT_PASSWORD']
                        teacher.unit = unit
                        db.session.add(teacher)
                try:
                    db.session.commit()
                    flash(u'老师更新成功')
                except:
                    db.rollback()
                    flash(u'未知错误')
            else:
                flash(u'文件格式错误!')
            return redirect(url_for('admin.index'))


admin.add_view(
    UserAdmin(
        db.session, category=u'用户管理', name=u'用户列表', url='user'
    )
)
admin.add_view(TeacherAdmin(url='import_teacher'))
