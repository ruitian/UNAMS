# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for
from app import app
from .. decorators import permission_required
from flask.ext.login import login_required, current_user
from .. models import Permission


@app.route('/')
def index():
    if current_user.is_authenticated():
        return redirect(url_for('competition'))
    return redirect(url_for('login'))
