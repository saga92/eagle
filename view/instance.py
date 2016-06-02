#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eagle import app, db
from flask import request, render_template, url_for, session, flash, redirect
import datetime
from utils import MessageQueue
from utils import logger
import json
from model import Instance
from model import User

@app.route('/create_instance', methods=['GET', 'POST'])
def create_instance():
    if request.method == 'POST':
        policy = {}
        policy['image_id'] = request.form['image_id']
        policy['container_name'] = request.form['container_name']
        policy['user_name'] = request.form['user_id']
        message = json.dumps(policy)
        MessageQueue.connect()
        MessageQueue.send(message)
        MessageQueue.disconnect()
    return render_template('dashboard.html')

@app.route('/update_ins', methods=['GET', 'POST'])
def update_instance_status():
    logger.info('update_instance_status')
    if request.method == 'POST':
        logger.info(request.form['container_serial'])
        user_query_result = User.query.filter(User.username == request.form.get('user_name')).first()
        user_id = user_query_result.id
        i = Instance(request.form.get('image_id'), \
            user_id, request.form.get('container_serial'), \
            request.form.get('status'))
        db.session.add(i)
        db.session.commit()
        logger.info('update_instance_status commit!')
    return 'succeed to update instance status'
