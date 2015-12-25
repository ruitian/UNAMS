# -*- coding: utf-8 -*-
from ... models import (
    UnitModel,
    UserModel,
    Competition,
    Student)
from flask import request, jsonify, redirect, url_for
from flask.ext.login import login_required

import json
from ... import app, db


@app.route('/department/_get')
@login_required
def getDepartment():
    units = UnitModel.query.all()
    return jsonify({'departments':
                    [unit.department_to_json() for unit in units]})


@app.route('/competition/_get_teacher')
@login_required
def getTeacher():
    id = request.args.get('id')
    teachers = UserModel.query.filter_by(user_name=id).first()
    print teachers
    return jsonify({
        'teacher_name': teachers.nick_name
    })


@app.route('/competition/_del_teacher')
@login_required
def delTeacher():
    id = request.args.get('id')
    teacher_id = request.args.get('teacher_id')
    competition = Competition.query.get(id)
    teacher = UserModel.query.filter_by(user_name=teacher_id).first()
    print teacher.id
    competition.teachers.remove(teacher)
    db.session.commit()
    return redirect(url_for('show_competition', id=id))


@app.route('/competition/_del_student')
@login_required
def delStudent():
    id = request.args.get('id')
    student_id = request.args.get('student_id')
    competition = Competition.query.get(id)
    student = Student.query.filter_by(student_id=student_id).first()
    competition.students.remove(student)
    db.session.commit()
    return redirect(url_for('show_competition', id=id))
