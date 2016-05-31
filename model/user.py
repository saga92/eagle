#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from eagle import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    is_deleted = db.Column(db.Integer)
