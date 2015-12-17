# _*_ coding: UTF-8 _*_
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babelex import Babel
from flask.ext.bootstrap import Bootstrap
from .config import config
import os

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
db = SQLAlchemy()
bootstrap = Bootstrap()

with app.app_context():
    config_name = os.getenv('FLASK_CONFIG') or 'default'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.app = app
    db.init_app(app)

    from .admin import admin
    admin.init_app(app)

    login_manager.setup_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'login'
    bootstrap.init_app(app)

from views import *
