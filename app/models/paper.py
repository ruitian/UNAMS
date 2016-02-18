# -*- coding: utf-8 -*-
from app import app, db
from wtforms.ext.sqlalchemy.orm import model_form


class PaperModel(db.Model):

    __tablename__ = 'paper'
    id = db.Column(db.Integer, primary_key=True)
    paper_title = db.Column(db.String(256), nullable=False)
    periodical = db.Column(db.String(256), nullable=False)
    level = db.Column(db.String(128))
    precedence = db.Column(db.String(128))
    issn = db.Column(db.String(128))
    student_name = db.Column(db.String(64))
    student_class = db.Column(db.String(64))
    acachemy = db.Column(db.String(64))
    public = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return self.paper_title

    @classmethod
    def model_form(cls, *args, **kwargs):
        return model_form(
            model=cls,
            db_session=db.session
        )
