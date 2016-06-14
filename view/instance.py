#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eagle import app, db
from flask import request, render_template, url_for, session, flash, redirect, jsonify
import datetime
from utils import MessageQueue
from utils import eagle_logger
import json
from model import Instance
from model import User

@app.route('/list_ins', methods=['GET'])
def list_instance():
    res = {}
    user_query_result = User.query.filter(User.username == request.args.get('signin_username')).first()
    if user_query_result is not None:
        instances = Instance.query.filter(Instance.user_id == user_query_result.id).all()
    ins_list = []
    eagle_logger.debug('list: %s' % request.args.get('signin_user_name'))
    for ins in instances:
        ins_item = {}
        ins_item['container_serial'] = ins.container_serial
        ins_item['container_name'] = ins.container_name
        ins_item['host'] = ins.host
        ins_item['port'] = ins.port
        ins_item['status'] = ins.status
        ins_list.append(ins_item)
    res['code'] = 'ok'
    res['instances'] = ins_list
    return jsonify(**res)

@app.route('/create_ins', methods=['GET', 'POST'])
def create_instance():
    res = {}
    if request.method == 'POST':
        req_data = json.loads(request.data)
        instance_query_result = Instance.query.filter(\
            Instance.container_name == req_data['container_name']).first()
        if instance_query_result is None:
            policy = {}
            policy['operate'] = app.config['CREATE_INSTANCE']
            policy['image_id'] = req_data['image_id']
            policy['container_name'] = req_data['container_name']
            policy['user_name'] = req_data['user_name']
            message = json.dumps(policy)
            MessageQueue.connect()
            MessageQueue.send(message)
            MessageQueue.disconnect()
            res['code'] = 'ok'
            res['message'] = 'creating docker VM'
            eagle_logger.info('creating your docker VM')
        else:
            res['code'] = 'err'
            res['message'] = 'container name occupied.'
            eagle_logger.info('container name occupied.')
    return jsonify(**res)

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
    res = {}
    if request.method == 'POST':
        req_data = json.loads(request.data)
        instance_query_result = Instance.query.filter(\
            Instance.container_serial == req_data['container_serial']).first()
        if instance_query_result is not None:
            policy = {}
            policy['operate'] = app.config['STOP_INSTANCE']
            policy['container_serial'] = req_data['container_serial']
            policy['user_name'] = req_data['user_name']
            message = json.dumps(policy)
            MessageQueue.connect()
            MessageQueue.send(message)
            MessageQueue.disconnect()
            res['code'] = 'ok'
            res['message'] = 'stoping your container'
        else:
            res['code'] = 'err'
            res['message'] = 'container not exist'
    return jsonify(**res)

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
    res = {}
    if request.method == 'POST':
        req_data = json.loads(request.data)
        instance_query_result = Instance.query.filter(\
            Instance.container_serial == req_data['container_serial']).first()
        if instance_query_result is not None:
            policy = {}
            policy['operate'] = app.config['REMOVE_INSTANCE']
            policy['container_serial'] = req_data['container_serial']
            policy['user_name'] = req_data['user_name']
            message = json.dumps(policy)
            MessageQueue.connect()
            MessageQueue.send(message)
            MessageQueue.disconnect()
            res['code'] = 'ok'
            res['message'] = 'removing your container'
        else:
            res['code'] = 'err'
            res['message'] = 'container not exist'
    return jsonify(**res)

@app.route('/remove_ins_res', methods=['GET', 'POST'])
def remove_instance_res():
    if request.method == 'POST':
        ins_to_rm = Instance.query.filter(\
            Instance.container_serial == request.form['container_serial']).first()
        db.session.delete(ins_to_rm)
        db.session.commit()
        eagle_logger.info('remove_instance_status commit!')
    return 'succeed to update instance status'

