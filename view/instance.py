#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eagle import app, db
from flask import request, render_template, url_for, session, flash, redirect
import datetime
from utils import MessageQueue
from utils import eagle_logger
import json
from model import Instance
from model import User

@app.route('/create_ins', methods=['GET', 'POST'])
def create_instance():
    popup = None
    if request.method == 'POST':
        instance_query_result = Instance.query.filter(\
            Instance.container_name == request.form['container_name']).first()
        if instance_query_result is None:
            policy = {}
            policy['operate'] = app.config['CREATE_INSTANCE']
            policy['image_id'] = request.form['image_id']
            policy['container_name'] = request.form['container_name']
            policy['user_name'] = request.form['user_id']
            message = json.dumps(policy)
            MessageQueue.connect()
            MessageQueue.send(message)
            MessageQueue.disconnect()
            popup = 'creating your docker VM'
        else:
            popup = 'container name occupied.'
    if popup is None:
        popup = 'some unknown problems occur.'
    return render_template('dashboard.html', popup=popup)

@app.route('/create_ins_res', methods=['GET', 'POST'])
def update_instance_status():
    eagle_logger.info('update_instance_status')
    if request.method == 'POST':
        eagle_logger.info(request.form['container_serial'])
        user_query_result = User.query.filter(User.username == request.form.get('user_name')).first()
        user_id = user_query_result.id
        i = Instance(request.form.get('image_id'), \
            user_id, request.form.get('container_name'), \
            request.form.get('container_serial'), \
            request.form.get('host'), request.form.get('port'),\
            request.form.get('status'))
        db.session.add(i)
        db.session.commit()
        eagle_logger.info('update_instance_status commit!')
    return 'succeed to update instance status'
