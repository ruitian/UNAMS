# -*- coding: utf-8 -*-
from flask import (
    request,
    render_template,
    flash,
    redirect,
    url_for,
    session
)
from ... models import UserModel
from ... forms import LoginForm
from flask.ext.login import login_required, login_user, logout_user
from ... import app, db


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit:
        user = UserModel.query.filter_by(user_name=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect('/')
        flash(u'用户名或密码错误！')
    return render_template('auth/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已退出系统')
    return redirect('/')
