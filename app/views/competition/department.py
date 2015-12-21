# -*- coding: utf-8 -*-
from ... models import UnitModel
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
