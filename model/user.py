#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import Base
from sqlalchemy import Column, Integer, String, DateTime

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    salt = Column(String(128), nullable=False)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime, nullable=False)
    is_deleted = Column(Integer, nullable=False)

    def __init__(self, username, password, *args, **kargs):
        self.username = username
        self.password = password
        self.email = kargs.get('email', '')
        self.salt = kargs.get('salt', '')
        self.create_time = kargs.get('create_time', '0000-00-00 00:00')
        self.update_time = kargs.get('update_time', '0000-00-00 00:00')
        self.is_deleted = kargs.get('is_deleted', 0)
