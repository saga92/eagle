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
            eagle_logger.info('creating your docker VM')
        else:
            eagle_logger.info('container name occupied.')
    return redirect(url_for('show_dashboard'))

@app.route('/create_ins_res', methods=['GET', 'POST'])
def create_instance_res():
    if request.method == 'POST':
        user_query_result = User.query.filter(User.username == request.form.get('user_name')).first()
        user_id = user_query_result.id
        i = Instance(request.form.get('image_id'), \
            user_id, request.form.get('container_name'), \
            request.form.get('container_serial'), \
            request.form.get('host'), request.form.get('port'),\
            request.form.get('status'))
        db.session.add(i)
        db.session.commit()
        eagle_logger.info('create_instance_res commit!')
    return 'succeed to update instance status'

@app.route('/stop_ins', methods=['GET', 'POST'])
def stop_instance():
    if request.method == 'POST':
        instance_query_result = Instance.query.filter(\
            Instance.container_serial == request.form['container_serial']).first()
        if instance_query_result is not None:
            policy = {}
            policy['operate'] = app.config['STOP_INSTANCE']
            policy['container_serial'] = request.form['container_serial']
            policy['user_id'] = request.form['user_id']
            message = json.dumps(policy)
            MessageQueue.connect()
            MessageQueue.send(message)
            MessageQueue.disconnect()
            eagle_logger.info('stoping your container')
        else:
            eagle_logger.info('container not exist')
    return redirect(url_for('show_dashboard'))

@app.route('/stop_ins_res', methods=['GET', 'POST'])
def stop_instance_res():
    if request.method == 'POST':
        instance_query_result = Instance.query.filter(\
            Instance.container_serial == request.form['container_serial']).first()
        instance_query_result.status = request.form['status']
        db.session.commit()
        eagle_logger.info('update_instance_status commit!')
    return 'succeed to update instance status'

@app.route('/remove_ins', methods=['GET', 'POST'])
def remove_instance():
    if request.method == 'POST':
        eagle_logger.info('xx1')
        instance_query_result = Instance.query.filter(\
            Instance.container_serial == request.form['container_serial']).first()
        if instance_query_result is not None:
            policy = {}
            policy['operate'] = app.config['REMOVE_INSTANCE']
            policy['container_serial'] = request.form['container_serial']
            policy['user_id'] = request.form['user_id']
            message = json.dumps(policy)
            MessageQueue.connect()
            MessageQueue.send(message)
            MessageQueue.disconnect()
            eagle_logger.info('removing your container')
        else:
            eagle_logger.info('container not exist')
    return redirect(url_for('show_dashboard'))

@app.route('/remove_ins_res', methods=['GET', 'POST'])
def remove_instance_res():
    if request.method == 'POST':
        ins_to_rm = Instance.query.filter(\
            Instance.container_serial == request.form['container_serial']).first()
        db.session.delete(ins_to_rm)
        db.session.commit()
        eagle_logger.info('remove_instance_status commit!')
    return 'succeed to update instance status'

