# -*- coding: utf-8 -*-
from app import app, db
from wtforms import widgets, fields
from wtforms.ext.sqlalchemy.orm import model_form


class PatentModel(db.Model):

    __tablename__ = 'patent'
    id = db.Column(db.Integer, primary_key=True)
    patent_title = db.Column(db.String(256), nullable=False)
    category = db.Column(db.Enum(
        *app.config['PATENT_CATEGORY'],
        name='patent_category_enum'
    ))
    student_name = db.Column(db.String(64))
    student_class = db.Column(db.String(64))
    precedence = db.Column(db.String(128))
    teacher_name = db.Column(db.String(64))
    patent_number = db.Column(db.String(128))
    certificate = db.Column(db.String(128))
    public = db.Column(db.Date, nullable=False)
    acachemy = db.Column(db.String(64))

    def __repr__(self):
        return self.patent_title

    @classmethod
    def model_form(cls, *args, **kwargs):
        return model_form(
            model=cls,
            db_session=db.session,
            field_args={
                'category': {'widget': widgets.Select()}
            }
        )
