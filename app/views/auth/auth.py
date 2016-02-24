# -*- coding: utf-8 -*-
from flask import (
    request,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    send_from_directory
)
from ... models import UserModel
from ... forms import LoginForm
from flask.ext.login import (
    login_required,
    login_user,
    current_user,
    logout_user
)
from app import app, db
import os


ALLOWED_EXTENSIONS = set(['jpg', 'png', 'gif', 'jpeg'])
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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


@app.route('/setting/profile', methods=['GET', 'POST'])
@login_required
def setting():
    return render_template('auth/profile.html')


@app.route('/setting/admin', methods=['GET', 'POST'])
@login_required
def setting_pass():
    return render_template('auth/pass.html')


@app.route('/update_prof_image', methods=['POST'])
@login_required
def update_profimage():
    if request.method == "POST":
        user = UserModel.query.filter_by(id=current_user.id).first()
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = "profile_%s.jpg" % current_user.id
            file_url = os.path.join(
                app.config['UPLOAD_FOLDER'], filename
            )
            file.save(file_url)
            user.user_image = True
            db.session.add(user)
            db.session.commit()
            print filename
        return filename


@app.route('/prof_image/<filename>')
@login_required
def prof_image(filename):
    return send_from_directory(
        UPLOAD_FOLDER, filename)


@app.route('/update_nickname', methods=['GET', 'POST'])
@login_required
def nick_name():
    if request.method == "POST":
        current_user.nick_name = request.form['nick_name']
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('setting'))


@app.route('/update_pass', methods=['GET', 'POST'])
@login_required
def user_pass():
    if request.method == "POST":
        user = UserModel.query.filter_by(id=current_user.id).first()
        old_pass = request.form['old_pass']
        if not user.verify_password(old_pass):
            flash(u'原密码不正确')
            return redirect(url_for('user_pass'))
        new_pass = request.form['new_pass']
        user.password = new_pass
        db.session.add(user)
        db.session.commit()
        flash(u'密码修改成功！请重新登陆系统')
        return redirect(url_for('logout'))
    return render_template('auth/pass.html')
