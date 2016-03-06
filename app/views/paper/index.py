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
PAPER_COVER_NAME = None
FILE_URL = None
FILES = []


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

        paper_cover_name = 'paper_cover%s.jpg' % paper.id
        url = app.config['UPLOAD_FOLDER'] + '/paper/covers'
        os.rename(
            url+os.sep+str(PAPER_COVER_NAME), url+os.sep+str(paper_cover_name))

        content_url = app.config['UPLOAD_FOLDER'] + '/paper/contents'
        for file in FILES:
            filename = secure_filename(file.filename)
            if os.path.splitext(file.filename)[1] == '.doc':
                paper_content_name = \
                    'paper_content_%s_%s.doc' % (paper.id, FILES.index(file))
            else:
                paper_content_name = \
                    'paper_content_%s_%s.jpg' % (paper.id, FILES.index(file))
            os.rename(
                content_url+os.sep+str(filename),
                content_url+os.sep+str(paper_content_name))

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
                app.config['UPLOAD_FOLDER']+'/paper/covers', filename)
            global PAPER_COVER_NAME
            PAPER_COVER_NAME = filename
            print PAPER_COVER_NAME
            files.save(file_url)
            return jsonify({
                'message': 'ok'
            })


@app.route('/upload_paper_content', methods=['POST'])
@login_required
def paper_content():
    if request.method == "POST":
        files = request.files.getlist("papers")
        global FILES
        for file in files:
            FILES.append(file)
            filename = secure_filename(file.filename)
            file_url = os.path.join(
                app.config['UPLOAD_FOLDER']+'/paper/contents', filename)
            file.save(file_url)
        return jsonify({
            'message': 'ok'
        })
