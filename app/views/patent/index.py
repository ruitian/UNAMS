# -*- coding: utf-8 -*-
# from ...forms import PatentForm
from ...models import PatentModel
from app import app, db
from flask.ext.login import login_required
from flask import render_template, request, redirect, flash


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
        flash(u'添加成功!')
        return redirect('/patent')
    return render_template('patent/patent.html', form=form)
