#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from eagle import db

class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    hashcode = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    is_deleted = db.Column(db.Integer, nullable=False)


class Instance(db.Model):
    __tablename__ = 'instance'
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    container_serial = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, nullable=False)
    is_deleted = db.Column(db.Integer, nullable=False)

    def __init__(self, image_id, user_id, container_serial, status, **kargs):
        self.image_id = image_id
        self.user_id = user_id
        self.container_serial = container_serial
        self.status = status
        self.create_time = kargs.get('create_time', '0000-00-00 00:00')
        self.update_time = kargs.get('update_time', '0000-00-00 00:00')
        self.is_deleted = kargs.get('is_deleted', 0)
