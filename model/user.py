#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from eagle import app, db

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

    def __init__(self, username, password, *args, **kargs):
        self.username = username
        self.password = password
        self.email = kargs.get('email', '')
        self.salt = kargs.get('salt', '')
        self.create_time = kargs.get('create_time', '0000-00-00 00:00')
        self.update_time = kargs.get('update_time', '0000-00-00 00:00')
        self.is_deleted = kargs.get('is_deleted', 0)
