# -*- coding: utf-8 -*-
from app import db
from wtforms import widgets, fields
from wtforms.ext.sqlalchemy.orm import model_form


class ProductionModel(db.Model):
    __tablename__ = 'production'
    id = db.Column(db.Integer, primary_key=True)
    pro_title = db.Column(db.String(64), nullable=False)
    pro_match = db.Column(db.String(64), nullable=True)
    pro_type = db.Column(db.String(64), nullable=True)
    pro_actor = db.Column(db.String(64), nullable=False)
    pro_time = db.Column(db.Date, nullable=False)
    pro_image = db.Column(
        db.String(254),
        nullable=True, default=None)

    def __repr__(self):
        return self.pro_title

    @classmethod
    def model_form(cls, *args, **kwargs):
        return model_form(
            model=cls,
            db_session=db.session,
        )
