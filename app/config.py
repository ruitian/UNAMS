# -*- coding: utf-8 -*-
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

    SECRET_KEY = 'you-will-never-guess'
    CSRF_ENABLED = True
    FLASK_POSTS_PER_PAGE = 10
    UPLOAD_FOLDER = BASE_DIR + '/uploads'
    BABEL_DEFAULT_LOCALE = 'zh_CN'
    DEFAULT_PASSWORD = '123'

    COMPETITION_LEVEL = (
        "国际级",
        "赛区级",
        "国家级",
        "省级"
    )
    COMPETITION_RATE = (
        "特等奖",
        "一等奖",
        "二等奖",
        "三等奖",
        "优秀奖",
        "金奖",
        "银奖",
        "铜奖",
    )
    PATENT_CATEGORY = (
        "实用新型",
        "发明专利",
        "外观设计"
    )

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
	USERNAME = os.getenv('MYSQL_USERNAME') or 'root'
	PASSWORD = os.getenv('MYSQL_PASSWORD') or 'password'
	HOST = os.getenv('MYSQL_PORT_3306_TCP_ADDR') or 'localhost'
	PORT = os.getenv('MYSQL_PORT_3306_TCP_PORT') or 3306
	DATABASE = os.getenv('MYSQL_INSTANCE_NAME') or 'unams'
    SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % 
				(USERNAME, PASSWORD, HOST, PORT, DATABASE)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/test_unams'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/unams'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
