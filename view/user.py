#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eagle import app
from flask import request, render_template, url_for, session, flash, redirect, jsonify
from model import User
from model import Instance
from utils import db
import hashlib
import time
import json
import random
import datetime
from sqlalchemy import or_
from utils import eagle_logger

@app.route('/', methods=['GET', 'POST'])
def show_dashboard():
    return render_template('index.html')

@app.route('/_session', methods=['GET'])
def get_from_session():
    key = request.args.get('key')
    eagle_logger.debug('session: %s ' % session.get(key))
    return str(session.get(key))

@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    res = {}
    if request.method == 'POST':
        req_data = json.loads(request.data)
        db_session = db.Session()
        result = db_session.query(User).filter(or_(User.username == req_data['username']\
            , User.email == req_data['username'])).first()
        if result is None:
            res['code'] = 'err'
            res['message'] = 'Username not found.'
        else:
            passcode = hashlib.md5(req_data['password'] + result.salt).hexdigest()
            if result.password == passcode:
                session['is_login'] = True
                session['signin_user_name'] = result.username
                instances = db_session.query(Instance).all()
                res['code'] = 'ok'
                res['message'] = 'sign in successful'
            else:
                res['code'] = 'err'
                res['message'] = 'wrong password.'
        return jsonify(**res)
    return render_template('index.html')

@app.route('/signout')
def sign_out():
    session.pop('is_login', None)
    session.pop('signin_user_name', None)
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    res = {}
    if request.method == 'POST':
        eagle_logger.debug(type(request.data))
        req_data = json.loads(request.data)
        db_session = db.Session()
        result = db_session.query(User).filter(User.username == req_data['username']).first()
        req_email =  req_data.get('email', None)
        if req_email is not None:
            result_mail = db_session.query(User).filter(User.email == req_email).first()
        if result is not None:
            res['code'] = 'err'
            res['message'] = 'Username have been occupied by others'
        elif req_email is not None and result_mail is not None:
            res['code'] = 'err'
            res['message'] = 'Email has been occupied by others'
        else:
            timestamp = str(time.time()) + str(random.randint(10000, 20000))
            salt = hashlib.md5(timestamp).hexdigest()
            passcode = hashlib.md5(req_data['password'] + salt).hexdigest()
            u = User(req_data['username'], passcode, email=req_data.get('email', ''), \
                salt=salt, create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
            db_session.add(u)
            db_session.commit()
            res['code'] = 'ok'
            res['message'] = 'sign up successful'
        return jsonify(**res)
    return render_template('index.html')
