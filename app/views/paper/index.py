# -*- coding: utf-8 -*-
from ...models import PaperModel
from app import app, db
from flask.ext.login import login_required
from flask import render_template, request, redirect, flash


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
        flash(u'添加信息成功！')
        return redirect('/paper')
    return render_template('paper/paper.html', form=form)
