# -*- coding: utf-8 -*-
from app import db


class ProductionModel(db.Model):
    __tablename__ = 'production'
    id = db.Column(db.Integer, primary_key=True)
    pro_title = db.Column(db.String(64), nullable=False)
    pro_match = db.Column(db.String(64), nullable=True)
    pro_type = db.Column(db.String(64), nullable=True)
    pro_actor = db.Column(db.String(64), nullable=False)
    pro_time = db.Column(
        db.TIMESTAMP, index=True,
        server_default=db.func.current_timestamp()
    )

    def __repr__(self):
        return self.pro_title
