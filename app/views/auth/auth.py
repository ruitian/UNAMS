# -*- coding: utf-8 -*-
from flask import (
    request,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    jsonify,
    send_from_directory
)
from ... models import(
    UserModel,
    CompTea,
    Project,
    Competition)
from ... forms import LoginForm
from flask.ext.login import (
    login_required,
    login_user,
    current_user,
    logout_user
)
from app import app, db
import os
import json


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
    return redirect('/login')


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
        verify_pass = request.form['verify_pass']
        if new_pass == verify_pass:
            user.password = new_pass
            db.session.add(user)
            db.session.commit()
            flash(u'密码修改成功！请重新登陆系统')
            return redirect(url_for('logout'))
        else:
            flash(u'两次密码不一致')
            return redirect(url_for('user_pass'))
    return render_template('auth/pass.html')


@app.route('/setting/user', methods=['GET', 'POST'])
@login_required
def show_user_pass():
    return render_template('auth/user_pass.html')


@app.route('/search_user', methods=['GET', 'POST'])
@login_required
def searchuser():
    if request.method == "POST":
        name = request.form['user_info']
        if len(name) == 0:
            #  判断管理员
            if current_user.id_role == 3:
                '''
                page = request.args.get('page', 1, type=int)
                pagination = UserModel.query.order_by(
                    UserModel.date_created.desc()).paginate(
                    page, per_page=app.config['FLASK_POSTS_PER_PAGE'],
                    error_out=False)
                users = pagination.items
                '''
                users = UserModel.query.all()
                return render_template('auth/user_pass.html',
                                       users=users)
            else:
                users = UserModel.query.filter_by(
                    id_unit=current_user.id_unit).all()
                return render_template('auth/user_pass.html', users=users)
        else:
            if current_user.id_role == 3:
                modify_user = UserModel.query.filter_by(
                    user_name=name).first()
                if modify_user is not None:
                    return render_template('auth/user_pass.html',
                                           modify_user=modify_user)
                flash(u'对不起，您输入有误！')
                return redirect(url_for('show_user_pass'))
            else:
                users = UserModel.query.filter_by(
                    id_unit=current_user.id_unit).all()
                search_user = UserModel.query.filter_by(
                    user_name=name).first()
                if search_user is not None:
                    for user in users:
                        if name == user.user_name:
                            modify_user = UserModel.query.filter_by(
                                user_name=name).first()
                            return render_template('auth/user_pass.html',
                                                   modify_user=modify_user)
                flash(u'对不起，您输入有误！')
                return redirect(url_for('show_user_pass'))
    return render_template('auth/user_pass.html')


@app.route('/update_userpass', methods=['GET', 'POST'])
@login_required
def update_user_pass():
    if request.method == "POST":
        user_name = request.form['user_name']
        new_pass = request.form['new_pass']
        user = UserModel.query.filter_by(user_name=user_name).first()
        user.password = new_pass
        db.session.add(user)
        db.session.commit()
        flash(u'密码修改成功！')
        redirect(url_for('show_user_pass'))
    return render_template('auth/user_pass.html')


@app.route('/show_pro', methods=['GET', 'POST'])
@login_required
def showPro():
    if current_user.role.role_name == '教师':
        comptea = CompTea.query.filter_by(teacher_id=current_user.id).first()
        if comptea is not None:
            competition = \
                Competition.query.filter_by(id=comptea.competition_id).first()
            project = Project.query.filter_by(
                id=competition.id_project).first()
            return render_template(
                'auth/user_pro.html',
                project=project,
                competition=competition)
        return render_template('auth/user_pro.html')

    elif current_user.role.role_name == '单位管理员':
        compteas = CompTea.query.all()
        teachers_id = []
        one_teachers_id = []
        #  get teachers
        for comptea in compteas:
            teachers_id.append(comptea.teacher_id)
        new_teachers_id = sorted(set(teachers_id), key=teachers_id.index)
        #  get one  alchemy teachers
        for new_teacher_id in new_teachers_id:
            user = UserModel.query.filter_by(id=new_teacher_id).first()
            if current_user.id_unit == user.id_unit:
                one_teachers_id.append(user.id)
        #  输出整个学院参与项目的所有老师
        teachers = []
        for teacher_id in one_teachers_id:
            user = UserModel.query.filter_by(id=teacher_id).first()
            teachers.append(user)
        for teacher in teachers:
            print teacher.nick_name
        return render_template('auth/user_pro.html', teachers=teachers)
    return render_template('auth/user_pro.html')


@app.route('/get_competition')
@login_required
def get_competitions():
    teacher_id = request.args.get('id')
    competitions = []
    compteas = CompTea.query.filter_by(
        teacher_id=teacher_id).all()
    for comptea in compteas:
        competition = Competition.query.filter_by(
            id=comptea.competition_id).first()
        competitions.append(competition)
    return jsonify({
        'competition': [
            competition.competition_to_json()
            for competition in competitions]
    })
