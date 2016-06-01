#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eagle import app, db
from flask import request, render_template, url_for, session, flash, redirect
import datetime
from utils import logger

@app.route('/create_instance', methods=['GET', 'POST'])
def create_instance():
    if request.method == 'POST':
        logger.info(request.form['image_id'])
    return render_template('dashboard.html')
