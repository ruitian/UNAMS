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
PAPER_CATALOGUE = []
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

        #  保存封面文件
        paper_cover_name = 'paper_cover%s.jpg' % paper.id
        cover_url = app.config['UPLOAD_FOLDER'] + '/paper/covers'
        os.rename(
            cover_url+os.sep+str(PAPER_COVER_NAME),
            cover_url+os.sep+str(paper_cover_name))

        #  保存目录文件
        catalogue_url = app.config['UPLOAD_FOLDER'] + '/paper/catalogue'
        for file in PAPER_CATALOGUE:
            filename = secure_filename(file.filename)
            paper_catalogue_name = \
                'paper_catalogue_%s_%s' % (
                    paper.id, PAPER_CATALOGUE.index(file))
            os.rename(
                catalogue_url+os.sep+str(filename),
                catalogue_url+os.sep+str(paper_catalogue_name))

        #  保存正文文件
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
            files.save(file_url)
            return jsonify({
                'message': 'ok'
            })


@app.route('/upload_paper_catalogue', methods=['POST'])
@login_required
def paper_catalogue():
    if request.method == "POST":
        files = request.files.getlist('paper-catalogue')
        global PAPER_CATALOGUE
        for file in files:
            if file and allowed_file(file.filename):
                PAPER_CATALOGUE.append(file)
                filename = secure_filename(file.filename)
                file_url = os.path.join(
                    app.config['UPLOAD_FOLDER']+'/paper/catalogue', filename)
                file.save(file_url)
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
            if file and allowed_file(file.filename):
                FILES.append(file)
                filename = secure_filename(file.filename)
                file_url = os.path.join(
                    app.config['UPLOAD_FOLDER']+'/paper/contents', filename)
                file.save(file_url)
        return jsonify({
            'message': 'ok'
        })
