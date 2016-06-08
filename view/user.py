#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eagle import app, db
from flask import request, render_template, url_for, session, flash, redirect
from model import User
from model import Instance
import hashlib
import time
import random
import datetime
from sqlalchemy import or_
from utils import eagle_logger

@app.route('/', methods=['GET', 'POST'])
def show_dashboard():
    eagle_logger.info('test')
    instances = None
    eagle_logger.info(session.get('signin_user_name'))
    user_query_result = User.query.filter(User.username == session.get('signin_user_name', '')).first()
    if user_query_result is not None:
        instances = Instance.query.filter(Instance.user_id == user_query_result.id).all()
    return render_template('dashboard.html', instances=instances)

@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    error = None
    if request.method == 'POST':
        result = User.query.filter(or_(User.username == request.form['username']\
            , User.email == request.form['username'])).first()
        if result is None:
            error = 'Username not found.'
        else:
            passcode = hashlib.md5(request.form['password'] + result.salt).hexdigest()
            if result.password == passcode:
                session['is_login'] = True
                session['signin_user_name'] = result.username
                flash('You have logged in')
                instances = Instance.query.all()
                return redirect(url_for('show_dashboard'))
            else:
                error = 'wrong password.'
    return render_template('signin.html', error=error)

@app.route('/signout')
def sign_out():
    session.pop('is_login', None)
    flash('You were logged out')
    return redirect(url_for('show_dashboard'))

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    error = None
    if request.method == 'POST':
        result = User.query.filter(User.username == request.form['username']).first()
        has_email =  request.form.get('email', None)
        if has_email is not None:
            result_mail = User.query.filter(User.email == request.form['email']).first()
        if result is not None:
            error = 'Username have been occupied by others'
        elif has_email is not None and result_mail is not None:
            error = 'Email has been occupied by others'
        else:
            timestamp = str(time.time()) + str(random.randint(10000, 20000))
            salt = hashlib.md5(timestamp).hexdigest()
            passcode = hashlib.md5(request.form['password'] + salt).hexdigest()
            u = User(request.form['username'], passcode, email=request.form.get('email', ''), \
                salt=salt, create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('sign_in'))
    return render_template('signup.html', error=error)
