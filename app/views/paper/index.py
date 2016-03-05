# -*- coding: utf-8 -*-
from ...models import PaperModel
from app import app, db
from flask.ext.login import login_required
from flask import (
    render_template,
    request,
    redirect,
    flash,
    jsonify
    )
from werkzeug import secure_filename
import os

ALLOWED_EXTENSIONS = set(['jpg', 'png', 'gif', 'jpeg'])
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
FILE_NAME = None
FILE_URL = None
FILE = None
FILES = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/paper', methods=['GET', 'POST'])
@login_required
def paper():
    PaperForm = PaperModel.model_form()
    form = PaperForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            return render_template('paper/paper.html', form=form)
        paper = PaperModel()
        form.populate_obj(paper)
        db.session.add(paper)
        db.session.commit()

        filename = 'paper_cover%s.jpg' % paper.id
        url = app.config['UPLOAD_FOLDER'] + '/paper'
        print FILE_NAME
        print url
        os.rename(url+os.sep+str(FILE_NAME), url+os.sep+str(filename))
        flash(u'添加信息成功！')
        return redirect('/paper')
    return render_template('paper/paper.html', form=form)


@app.route('/upload_paper_cover', methods=['POST'])
@login_required
def paper_cover():
    if request.method == "POST":
        files = request.files['paper-cover']
        if files and allowed_file(files.filename):
            filename = secure_filename(files.filename)
            file_url = os.path.join(
                app.config['UPLOAD_FOLDER']+'/paper', filename)
            global FILE_NAME
            FILE = files
            FILE_NAME = filename
            files.save(file_url)
            return jsonify({
                'message': 'ok'
            })
