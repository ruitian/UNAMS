# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for
from app import app
from .. decorators import permission_required
from flask.ext.login import login_required
from .. models import Permission


@app.route('/')
@login_required
def index():
    return redirect(url_for('competition'))


@app.route('/test')
@login_required
@permission_required(Permission.ADMINISTER)
def for_only():
    return "for sfsdfsdf"
