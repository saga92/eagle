#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import db
from model import User

def update_col_by_id(id, *args, **kwargs):
    db_session = db.Session()
    user_query_res = db_session.query(User).filter(User.id == id).first()
    for key in kwargs:
        setattr(user_query_res, key, kwargs.get(key))
    db_session.commit()

def update_password_by_id(id, password):
    update_user(id, password=password)

def update_email_by_id(id, email):
    update_user(id, email=email)

def update_salt_by_id(id, salt):
    update_user(id, salt=salt)

def update_create_time_by_id(id, create_time):
    update_user(id, create_time=create_time)

def update_update_time_by_id(id, update_time):
    update_user(id, update_time=update_time)

def update_is_deleted_by_id(id, is_deleted):
    update_user(id, is_deleted=is_deleted)
