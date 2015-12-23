# -*- coding: utf-8 -*-
from ... models import UnitModel, UserModel
from flask import request, jsonify
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
