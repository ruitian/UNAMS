# -*- coding: utf-8 -*-
from app import app, db
from flask import (
    request,
    flash,
    render_template,
    redirect,
    send_from_directory,
    jsonify)
from ...models import ProductionModel
from flask.ext.login import login_required
from werkzeug import secure_filename
import os


ALLOWED_EXTENSIONS = set(['jpg', 'png', 'gif', 'jpeg', 'doc', 'xls'])
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER'] + '/production'
IMAGE_NAME = None
DOC_NAME = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload_proimg', methods=['POST'])
@login_required
def upload_proimg():
    if request.method == "POST":
        files = request.files['pro_img']
        if files and allowed_file(files.filename):
            filename = secure_filename(files.filename)
            file_url = os.path.join(
                app.config['UPLOAD_FOLDER']+'/production/imgs', filename)
            files.save(file_url)
            file_size = os.path.getsize(file_url)
            global IMAGE_NAME
            IMAGE_NAME = filename
        return jsonify({
            'message': 'ok'
        })


@app.route('/production', methods=['GET', 'POST'])
@login_required
def production():
    ProductionForm = ProductionModel.model_form()
    form = ProductionForm(request.form)
    if request.method == "POST":
        if not form.validate():
            return render_template('production/production.html', form=form)
        production = ProductionModel()
        form.populate_obj(production)
        production.pro_image = IMAGE_NAME
        db.session.add(production)
        db.session.commit()
        flash(u'添加成功!')
        return redirect('/production')
    return render_template('production/production.html', form=form)


@app.route('/uploads/production/<filename>')
@login_required
def upload_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
