#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import db
from model import User

def update_password(id, password):
    update_user(id, password=password)

def update_email(id, email):
    update_user(id, email=email)

def update_salt(id, salt):
    update_user(id, salt=salt)

def update_create_time(id, create_time):
    update_user(id, create_time=create_time)

def update_update_time(id, update_time):
    update_user(id, update_time=update_time)

def update_is_deleted(id, is_deleted):
    update_user(id, is_deleted=is_deleted)

def update_user(id, *args, **kwargs):
    db_session = db.Session()
    user_query_res = db_session.query(User).filter(User.id == id).first()
    for key, value in kwargs:
        getattr(user_query_res, key) = kwargs.get(key)
    db_session.commit()

