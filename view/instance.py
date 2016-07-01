#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eagle import app
from flask import request, render_template, url_for, session, flash, redirect, jsonify
import datetime
from utils import UiQueue
from utils import eagle_logger, ui_logger
import json
from model import Instance
from model import Image
from model import User
from utils import db

@app.route('/list_ins', methods=['GET'])
def list_instance():
    res = {}
    instances = []
    db_session = db.Session()
    user_query_result = db_session.query(User).filter(User.username == request.args.get('signin_username')).first()
    if user_query_result is not None:
        instances = db_session.query(Instance, Image).\
                join(Image, Instance.image_id == Image.id).filter(Instance.user_id == user_query_result.id).all()
    ins_list = []
    for ins, img in instances:
        ins_item = {}
        ins_item['image_id'] = ins.image_id
        ins_item['image_name'] = img.image_name
        ins_item['container_serial'] = ins.container_serial
        ins_item['container_name'] = ins.container_name
        ins_item['host'] = ins.host
        ins_item['port'] = ins.port
        ins_item['status'] = ins.status
        ins_item['jump_server'] = ins.jump_server
        ins_list.append(ins_item)
    ui_logger.info('len(instances) == %s' % str(len(instances)))
    res['code'] = 'ok'
    res['instances'] = ins_list
    return jsonify(**res)

@app.route('/create_ins', methods=['GET', 'POST'])
def create_instance():
    res = {}
    if request.method == 'POST':
        req_data = json.loads(request.data)
        db_session = db.Session()
        instance_query_result = db_session.query(Instance).filter(\
            Instance.container_name == req_data['container_name']).first()
        if instance_query_result is None:
            policy = {}
            policy['operate'] = app.config['CREATE']
            policy['image_id'] = req_data['image_id']
            policy['container_name'] = req_data['container_name']
            policy['user_name'] = req_data['user_name']
            message = json.dumps(policy)
            ui_mq = UiQueue()
            #blocking max time: 60s
            worker_res = ui_mq.send(message)
            worker_res_dict = json.loads(worker_res)
            res['code'] = worker_res_dict['code']
            res['message'] = worker_res_dict['message']
            res['instance'] = worker_res_dict['ins']
            eagle_logger.info(res['message'])
            eagle_logger.info('db add instance commit!')
        else:
            res['code'] = 'err'
            res['message'] = 'container name occupied.'
            eagle_logger.info('container name occupied.')
    return jsonify(**res)

@app.route('/stop_ins', methods=['GET', 'POST'])
def stop_instance():
    res = {}
    if request.method == 'POST':
        req_data = json.loads(request.data)
        db_session = db.Session()
        instance_query_result = db_session.query(Instance).filter(\
            Instance.container_serial == req_data['container_serial']).first()
        if instance_query_result is not None:
            policy = {}
            policy['operate'] = app.config['STOP']
            policy['container_serial'] = req_data['container_serial']
            policy['container_name'] = instance_query_result.container_name
            policy['user_name'] = req_data['user_name']
            message = json.dumps(policy)
            ui_mq = UiQueue()
            worker_res = ui_mq.send(message)
            worker_res_dict = json.loads(worker_res)
            res['code'] = worker_res_dict['code']
            res['message'] = worker_res_dict['message']
            res['container_serial'] = worker_res_dict['container_serial']
            eagle_logger.info(res['message'])
        else:
            res['code'] = 'err'
            res['message'] = 'container not exist'
    return jsonify(**res)

@app.route('/restart_ins', methods=['GET', 'POST'])
def restart_instance():
    res = {}
    if request.method == 'POST':
        req_data = json.loads(request.data)
        db_session = db.Session()
        instance_query_result = db_session.query(Instance).filter(\
            Instance.container_serial == req_data['container_serial']).first()
        if instance_query_result is not None:
            policy = {}
            policy['operate'] = app.config['RESTART']
            policy['container_serial'] = req_data['container_serial']
            policy['container_name'] = instance_query_result.container_name
            policy['user_name'] = req_data['user_name']
            message = json.dumps(policy)
            ui_mq = UiQueue()
            worker_res = ui_mq.send(message)
            worker_res_dict = json.loads(worker_res)
            res = worker_res_dict
            eagle_logger.info(res['message'])
        else:
            res['code'] = 'err'
            res['message'] = 'container not exist'
    return jsonify(**res)

@app.route('/remove_ins', methods=['GET', 'POST'])
def remove_instance():
    res = {}
    if request.method == 'POST':
        req_data = json.loads(request.data)
        db_session = db.Session()
        instance_query_result = db_session.query(Instance).filter(\
            Instance.container_serial == req_data['container_serial']).first()
        if instance_query_result is not None:
            policy = {}
            policy['operate'] = app.config['REMOVE']
            policy['container_serial'] = req_data['container_serial']
            policy['user_name'] = req_data['user_name']
            message = json.dumps(policy)
            ui_mq = UiQueue()
            worker_res = ui_mq.send(message)
            worker_res_dict = json.loads(worker_res)
            res['code'] = worker_res_dict['code']
            res['message'] = worker_res_dict['message']
            res['container_serial'] = worker_res_dict['container_serial']
            eagle_logger.info(res['message'])
        else:
            res['code'] = 'err'
            res['message'] = 'container not exist'
    return jsonify(**res)

