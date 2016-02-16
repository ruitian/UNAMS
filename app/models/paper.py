# -*- coding: utf-8 -*-
from app import app, db


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
