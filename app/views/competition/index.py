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
    Student,
    Grade,
    Project,
    Competition,
    Adviser,
    Participant,
    UnitModel,
    MajorModel
)
from flask.ext.login import login_required

from ... import app, db
from ...forms import StudentForm
import os


ALLOWED_EXTENSIONS = set(['jpg'])


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
        return redirect(url_for('show_competition', id=competition.id))
    return render_template('competition/competition.html', form=form)


@app.route('/show_competition/<int:id>')
@login_required
def show_competition(id):
    competition = Competition.query.filter_by(id=id).first_or_404()
    student_form = StudentForm()
    return render_template('competition/show_competition.html',
                           competition=competition,
                           student_form=student_form, id=id)


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
    print major
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
    except:
        flash(u'未知错误')
        db.session.rollback()
    return redirect(url_for('show_competition', id=id))
