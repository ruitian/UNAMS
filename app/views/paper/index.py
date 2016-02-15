# -*- coding: utf-8 -*-
from ...forms import PaperForm
from app import app
from flask.ext.login import login_required
from flask import render_template, request, redirect


@app.route('/paper', methods=['GET', 'POST'])
@login_required
def paper():
    form = PaperForm()
    if request.method == 'POST' and form.validate_on_submit:
        title = form.public.data
        print title
        return redirect('/')
    return render_template('paper/paper.html', form=form)
