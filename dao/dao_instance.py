#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import db
from model import Instance, User
import worker_cfg

def update_status_by_serial(container_serial, status):
	db_session = db.Session()
	instance_query_res = db_session.query(Instance).filter(Instance.container_serial == container_serial).first()
	instance_query_res.status = status
	db_session.commit()

def update_host_by_serial(container_serial, host):
	db_session = db.Session()
	instance_query_res = db_session.query(Instance).filter(Instance.container_serial == container_serial).first()
	instance_query_res.host = host
	db_session.commit()

def update_port_by_serial(container_serial, port):
	db_session = db.Session()
	instance_query_res = db_session.query(Instance).filter(Instance.container_serial == container_serial).first()
	instance_query_res.port = port
	db_session.commit()

def create_instance(container_serial, *args, **kwargs):
	db_session = db.Session()
	user_query_res = db_session.query(User).filter(User.username == kwargs.get('user_name')).first()
	user_id = user_query_res.id
	host = ''
	port = 0
	ins = Instance(kwargs.get('image_id'), user_id, kwargs.get('container_name'), container_serial, host, port, worker_cfg.STOP_INSTANCE)
	db_session.add(ins)
	db_session.commit()

def remove_instance(container_serial):
	db_session = db.Session()
	instance_query_res = db_session.query(Instance).filter(Instance.container_serial == container_serial).first()
	container_name = instance_query_res.container_name
	db_session.delete(instance_query_res)
	db_session.commit()
	return container_name