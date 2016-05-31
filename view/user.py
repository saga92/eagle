#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eagle import app
from flask import request, render_template, url_for, session, flash, redirect
from model import User

@app.route('/', methods=['GET', 'POST'])
def show_dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        result = User.query.filter(User.username == request.form['username'] and User.password == request.form['password']).first()
        if result is None:
            error = 'Invalid username or Invalid password'
        else:
            session['is_login'] = True
            flash('You have logged in')
            return redirect(url_for('show_dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('is_login', None)
    flash('You were logged out')
    return redirect(url_for('show_dashboard'))
