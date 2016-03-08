# -*- coding: utf-8 -*-
# from ...forms import PatentForm
from ...models import PatentModel
from app import app, db
from flask.ext.login import login_required
from flask import render_template, request, redirect, flash

from werkzeug import secure_filename
import os

ALLOWED_EXTENSIONS = set(['doc', 'xls'])
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/patent', methods=['GET', 'POST'])
@login_required
def patent():
    PatentForm = PatentModel.model_form()
    form = PatentForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            return render_template('patent/patent.html', form=form)
        patent = PatentModel()
        form.populate_obj(patent)
        db.session.add(patent)
        db.session.commit()
        files = request.files['annex']
        if files and allowed_file(files.filename):
            print files.filename
            filename = 'patent_%d.doc' % patent.id
            file_url = os.path.join(
                app.config['UPLOAD_FOLDER']+'/patent', filename)
            files.save(file_url)
        flash(u'添加成功!')
        return redirect('/patent')
    return render_template('patent/patent.html', form=form)
