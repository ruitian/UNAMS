# -*- coding: utf-8 -*-
from flask import(
    render_template,
    flash,
    redirect,
    url_for,
    request,
    current_app,
    abort,
    json,
    send_from_directory
)
from ... models import (
    UserModel,
    Grade,
    Project,
    Competition,
    Adviser,
    Participant,
    UnitModel,
    Student,
    MajorModel,
    CompTea
)
from flask.ext.login import login_required, current_user

from ... import app, db
from ...forms import StudentForm
import os


ALLOWED_EXTENSIONS = set(['jpg'])
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/competition', methods=['GET', 'POST'])
@login_required
def competition():
    CompetitionForm = Competition.model_form()
    form = CompetitionForm(request.form)
    if request.method == 'POST':

        if not form.validate():
            return render_template('competition/competition.html', form=form)
        competition = Competition()
        form.populate_obj(competition)
        db.session.add(competition)
        db.session.commit()

        file = request.files['file']
        if file and allowed_file(file.filename):
            file.filename = 'competition_%s.jpg' % competition.id
            file_url = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_url)
        return redirect(url_for('show_competition',
                                username=current_user.user_name,
                                id=competition.id))
    return render_template('competition/competition.html', form=form)


@app.route('/competition/<username>/<int:id>')
@login_required
def show_competition(username, id):
    teachers = []
    if username != current_user.user_name and username != 'admin':
        return redirect(url_for('competition'))
    compteas = CompTea.query.filter_by(competition_id=id).all()
    for comptea in compteas:
        teacher = UserModel.query.filter_by(id=comptea.teacher_id).first()
        teachers.append(teacher)
    competition = Competition.query.filter_by(id=id).first_or_404()
    student_form = StudentForm()
    return render_template('competition/show_competition.html',
                           competition=competition,
                           teachers=teachers,
                           student_form=student_form, id=id)


@app.route('/uploads/competition/<int:id>')
@login_required
def uploaded_file(id):
    competition = Competition.query.filter_by(id=id).first_or_404()
    return send_from_directory(UPLOAD_FOLDER,
                               'competition_%s.jpg' % competition.id)


@app.route('/competition/<int:id>/participant', methods=['POST'])
@login_required
def participant(id):
    competition = Competition.query.filter_by(id=id).first_or_404()
    StudentForm = Student.model_form()
    form = StudentForm()  # noqa
    return redirect(url_for('show_competition', id=competition.id))


@app.route('/add_student', methods=['POST'])
@login_required
def add_student():
    student_id = request.form['student_id']
    student_name = request.form['student_name'].encode('utf-8')
    id_grade = request.form['id_grade']
    id_acachemy = int(request.form['id_acachemy'])
    id_major = int(request.form['id_major'])
    id = request.form['competition_id']
    grade = Grade.query.filter_by(grade_name=id_grade).first()
    acachemy = UnitModel.query.filter_by(id=id_acachemy).first()
    major = MajorModel.query.filter_by(id=id_major).first()
    competition = Competition.query.filter_by(id=id).first()
    student = Student.query.filter_by(student_id=student_id).first()
    if student is None:
        student = Student(
            student_id=student_id,
            student_name=student_name,
            grade=grade,
            unit=acachemy,
            major=major
        )
        db.session.add(student)
        try:
            db.session.commit()
            student = Student.query.filter_by(student_id=student_id).first()
        except:
            flash(u'未知错误')
            db.session.rollback()
            db.session.commit()
    competition = Competition.query.get(id)
    competition.students.append(student)
    db.session.commit()
    return redirect(url_for('show_competition', id=id))


@app.route('/add_teacher', methods=['POST'])
@login_required
def add_teacher():
    teacher_id = request.form['teacher_id']
    id = request.form['competition_id']
    teacher = UserModel.query.filter_by(user_name=teacher_id).first()
    competition = Competition.query.get(id)
    # competition.teachers.append(teacher)
    comptea = CompTea(competitions=competition, teachers=teacher)
    db.session.add(comptea)
    db.session.commit()
    return redirect(url_for(
        'show_competition',
        username=current_user.user_name, id=id))
