# -*- coding: utf-8 -*-
from .mixin import ModelViewMixin, BaseViewMixin
from flask import redirect, request, url_for, flash, views
from ..models import UnitModel, MajorModel, Grade
from .. import app, db
from . import admin
from flask.ext.admin import expose_plugview
from datetime import datetime
from werkzeug import secure_filename
import os
import xlrd


ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class GradeAdmin(ModelViewMixin):

    def __init__(self, session, **kwargs):
        super(GradeAdmin, self).__init__(Grade, session, **kwargs)

    def scaffold_form(self):
        form_class = super(GradeAdmin, self).scaffold_form()
        return form_class


class UnitAdmin(ModelViewMixin):
    labels = dict(
        id='#',
        unit_id='单位/学院编号',
        unit_name='单位/学院名称'
    )
    column_labels = labels
    column_list = ['id', 'unit_id', 'unit_name']
    can_edit = False
    list_template = 'admin/department.html'

    def __init__(self, session, **kwargs):
        super(UnitAdmin, self).__init__(UnitModel, session, **kwargs)

    def scaffold_form(self):
        form_class = super(UnitAdmin, self).scaffold_form()
        return form_class


class UnitsAdmin(BaseViewMixin):
    def is_visible(self):
        return False

    @expose_plugview('/')
    class ImportUnit(views.MethodView):
        def post(self, cls):
            now = datetime.utcnow()
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = now.strftime('units%Y%m%d.xls')
                file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_url)
                bk = xlrd.open_workbook(file_url)
                sh = bk.sheets()[0]
                for i in range(1, sh.nrows):
                    try:
                        unit_id = int(sh.row(i)[0].value.encode('utf-8'))
                        unit_name = sh.row(i)[1].value.encode('utf-8')
                        major_id = sh.row(i)[2].value.encode('utf-8')
                        major_name = sh.row(i)[3].value.encode('utf-8')
                    except:
                        flash(u'更新数据失败,错误数据为%s行' % i)
                        db.session.rollback()
                        break
                    unit = UnitModel.query.filter_by(
                        unit_id=unit_id, unit_name=unit_name).first()
                    major = MajorModel.query.filter_by(
                        major_id=major_id, major_name=major_name).first()
                    if not unit:
                        unit = UnitModel(unit_id=unit_id, unit_name=unit_name)
                        db.session.add(unit)
                    if not major:
                        major = MajorModel(
                            major_id=major_id,
                            major_name=major_name, unit=unit)
                        db.session.add(major)
                try:
                    db.session.commit()
                    flash(u'单位信息更新成功')
                except:
                    flash(u'未知错误')
                    db.session.rollback()
            else:
                flash(u'文件类型错误!')
            return redirect(url_for('admin.index'))


class MajorAdmin(ModelViewMixin):
    labels = dict(
        id='#',
        major_id=u'专业编号',
        major_name=u'专业名称',
        unit=u'学院'
    )
    column_labels = labels
    column_list = ['id', 'major_id', 'major_name', 'unit']
    can_edit = False

    def __init__(self, session, **kwargs):
        super(MajorAdmin, self).__init__(MajorModel, session, **kwargs)

    def scaffold_form(self):
        form_class = super(MajorAdmin, self).scaffold_form()
        return form_class

admin.add_view(
    GradeAdmin(
        db.session, category=u'信息管理', name=u'年级管理', url='grade'
    )
)
admin.add_view(
    UnitAdmin(
        db.session, category=u'信息管理', name=u'院系列表', url='unit')
)
admin.add_view(
    MajorAdmin(
        db.session, category=u'信息管理', name=u'专业列表', url='major'
    )
)

admin.add_view(UnitsAdmin(url='import_unit'))
