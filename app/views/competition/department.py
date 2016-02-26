# -*- coding: utf-8 -*-
from ... models import (
    UnitModel,
    MajorModel,
    UserModel,
    Competition,
    Grade,
    Student,
    CompTea)
from flask import request, jsonify, redirect, url_for
from flask.ext.login import login_required, current_user

import json
from ... import app, db


@app.route('/department/_get')
@login_required
def getDepartment():
    units = UnitModel.query.all()
    return jsonify({'departments':
                    [unit.department_to_json() for unit in units]})


@app.route('/competition/_get_grade')
@login_required
def getGrade():
    grades = Grade.query.all()
    return jsonify({'grades':
                   [grade.grade_to_json() for grade in grades]})


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
    '''
    teacher_id = request.args.get('teacher_id')
    competition = Competition.query.get(id)
    teacher = UserModel.query.filter_by(user_name=teacher_id).first()
    competition.teachers.remove(teacher)
    db.session.commit()
    '''
    id = request.args.get('id')
    teacher_id = request.args.get('teacher_id')
    comptea = CompTea.query.filter_by(teacher_id=teacher_id).first()
    db.session.delete(comptea)
    db.session.commit()
    return redirect(url_for(
        'show_competition',
        username=current_user.user_name,
        id=id))


@app.route('/competition/_del_student')
@login_required
def delStudent():
    id = request.args.get('id')
    student_id = request.args.get('student_id')
    competition = Competition.query.get(id)
    student = Student.query.filter_by(student_id=student_id).first()
    competition.students.remove(student)
    db.session.commit()
    return redirect(url_for(
        'show_competition',
        username=current_user.user_name,
        id=id))


@app.route('/competition/_edit_student', methods=['POST'])
@login_required
def editStudent():
    id = request.form['competition_id']
    student_old_id = request.form['student_old_id']
    student_id = request.form['student_id']
    student_name = request.form['student_name']
    grade = request.form['student_grade']
    acachemy_id = int(request.form['edit_student_acachemy_hi'])
    major_id = int(request.form['edit_student_major_hi'])

    grade = Grade.query.filter_by(grade_name=grade).first()
    acachemy = UnitModel.query.filter_by(id=acachemy_id).first()
    major = MajorModel.query.filter_by(id=major_id).first()
    student = Student.query.filter_by(student_id=student_old_id).first()
    student.student_id = student_id
    student.student_name = student_name
    student.grade = grade
    student.unit = acachemy
    student.major = major
    db.session.add(student)
    try:
        db.session.commit()
    except:
        flash(u'未知错误')
        db.session.rollback()
    return redirect(url_for(
        'show_competition',
        username=current_user.user_name,
        id=id))
