#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import db
from model import User

def updatePassword(id, password):
    db_session = db.Session()
    user_query_res = db_session.query(User).filter(User.id == id).first()
    user_query_res.password = password
    db_session.commit()

def updateEmail(id, email):
    db_session = db.Session()
    user_query_res = db_session.query(User).filter(User.id == id).first()
    user_query_res.email = email
    db_session.commit()

def updateSalt(id, salt):
    db_session = db.Session()
    user_query_res = db_session.query(User).filter(User.id == id).first()
    user_query_res.salt = salt
    db_session.commit()

def updateCreateTime(id, create_time):
    db_session = db.Session()
    user_query_res = db_session.query(User).filter(User.id == id).first()
    user_query_res.create_time = create_time
    db_session.commit()

def updateUpdateTime(id, update_time):
    db_session = db.Session()
    user_query_res = db_session.query(User).filter(User.id == id).first()
    user_query_res.update_time = update_time
    db_session.commit()

def updateIsDeleted(id, is_deleted):
    db_session = db.Session()
    user_query_res = db_session.query(User).filter(User.id == id).first()
    user_query_res.is_deleted = is_deleted
    db_session.commit()



