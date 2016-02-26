# -*- coding: utf-8 -*-
from app import app, db


class CompTea(db.Model):
    __tablename__ = 'comptea'
    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True)
    competition_id = db.Column(
        db.Integer,
        db.ForeignKey('competition.id'),
        primary_key=True)
