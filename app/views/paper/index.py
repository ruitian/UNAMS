# -*- coding: utf-8 -*-
from ...forms import PaperForm
from ...models import PaperModel
from app import app, db
from flask.ext.login import login_required
from flask import render_template, request, redirect


@app.route('/paper', methods=['GET', 'POST'])
@login_required
def paper():
    form = PaperForm()
    if request.method == 'POST' and form.validate_on_submit:
        title = form.public.data
        paper = PaperModel(
            paper_title=form.paper_title.data,
            periodical=form.periodical.data,
            level=form.level.data,
            precedence=form.precedence.data,
            issn=form.issn.data,
            student_name=form.student_name.data,
            student_class=form.grade.data,
            acachemy=form.acachemy.data,
            public=form.public.data
        )
        db.session.add(paper)
        db.session.commit()
        return redirect('/')
    return render_template('paper/paper.html', form=form)
