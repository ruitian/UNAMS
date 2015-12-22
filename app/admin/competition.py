# -*- coding: utf-8 -*-
from .mixin import ModelViewMixin, BaseViewMixin
from flask import redirect, request, url_for, flash, views
from ..models import Project, Competition, Student
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


class ProjectAdmin(ModelViewMixin):

    labels = dict(
        id='#',
        project_name=u'项目名称',
        date_created=u'创建日期'
    )
    column_labels = labels
    list_template = 'admin/competition_project.html'

    def __init__(self, session, **kwargs):
        super(ProjectAdmin, self).__init__(Project, session, **kwargs)

    def scaffold_form(self):
        form_class = super(ProjectAdmin, self).scaffold_form()
        return form_class


class CompetitionAdmin(ModelViewMixin):
    labels = dict(
        id=u'#',
        project=u'竞赛项目',
        project_name=u'项目名称',
        achievement_name=u'成果名称',
        winning_level=u'获奖级别',
        rate=u'等级',
        awards_unit=u'颁奖单位',
        winning_time=u'获奖时间',
        students=u'学生',
        is_review=u'是否审核',
        participants=u'参赛学生',
        advisers=u'指导教师',
        date_created=u'创建时间'
        )

    column_labels = labels
    can_restore = False
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True
    create_modal = True
    list_template = 'admin/competition_list.html'
    column_list = ('id', 'project', 'achievement_name',
                   'winning_level', 'rate',
                   'awards_unit', 'winning_time',
                   'is_review', 'date_created')

    column_filters = ['project', 'achievement_name',
                      'winning_level', 'rate',
                      'awards_unit', 'winning_time', 'is_review']

    column_editable_list = ['is_review']

    def __init__(self, session, **kwargs):
        super(CompetitionAdmin, self).__init__(Competition, session, **kwargs)

    def scaffold_form(self):
        form_class = super(CompetitionAdmin, self).scaffold_form()
        return form_class


class ImportProjectView(BaseViewMixin):

    def is_visible(self):
        return False

    @expose_plugview('/')
    class ImportProject(views.MethodView):
        def post(self, cls):
            now = datetime.utcnow()
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = now.strftime('projects%Y%m%d.xls')
                file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_url)
                bk = xlrd.open_workbook(file_url)
                sh = bk.sheets()[0]
                for i in range(1, sh.nrows):
                    try:
                        project_name = sh.row(i)[0].value.encode('utf-8')
                    except:
                        flash(u'数据更新失败，错误数据为%s行' % i)
                        db.session.rollback()
                        break
                    project = Project.query.filter_by(
                        project_name=project_name).first()
                    if not project:
                        project = Project(project_name=project_name)
                        db.session.add(project)
                try:
                    db.session.commit()
                    flash(u'竞赛项目更新成功')
                except:
                    flash(u'未知错误')
                    db.session.rollback()
            else:
                flash(u'文件类型错误')
            return redirect(url_for('admin.index'))

admin.add_view(
    CompetitionAdmin(
        db.session, category=u'竞赛管理', name='竞赛列表'
    )
)
admin.add_view(
    ProjectAdmin(
        db.session, category=u'竞赛管理', name=u'竞赛项目'
    )
)

admin.add_view(
    ImportProjectView(url='import_project')
)
