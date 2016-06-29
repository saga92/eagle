#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from utils import WorkerQueue
from utils import worker_logger
from utils import db
from model import Instance, User, Image
import requests
import worker_cfg
import docker
from dao import *
import traceback

def worker_handler(message):
    policy = json.loads(message)
    cli = connect_docker_cli()
    if policy['operate'] == worker_cfg.CREATE:
        res = create_run_container(cli, **policy)
    elif policy['operate'] == worker_cfg.STOP:
        res = stop_container(cli, **policy)
    elif policy['operate'] == worker_cfg.RESTART:
        res = restart_container(cli, **policy)
    elif policy['operate'] == worker_cfg.REMOVE:
        res = remove_container(cli, **policy)
    return res

def connect_docker_cli():
    if worker_cfg.MAC:
        import docker
        cli = docker.from_env(assert_hostname=False)
    else:
        from docker import Client
        cli = Client(base_url=worker_cfg.DOCKER_CLI_URL)
    return cli

def create_run_container(cli, *args, **kwargs):
    res = create_container(cli, *args, **kwargs)
    res_dict = json.loads(res)
    if (res_dict['code'] == 'error'):
        return res

    res = run_container(cli, **res_dict)
    return res

def create_container(cli, *args, **kwargs):
    res = {'code': 'error', 'message': 'problem error'}
    image_id = kwargs.get('image_id')
    image_name = worker_cfg.IMAGE_DICT.get(image_id)
    try:
        container = cli.create_container(image=image_name, detach=True, name=kwargs.get('container_name'))
    except docker.errors.APIError:
        res['ins'] = {}
        msg = traceback.format_exc()
        msg = msg[msg.find('APIError:'):]
        worker_logger.error("failed to create %s. %s" % (kwargs.get('container_name'), msg))
        return json.dumps(res)

    #write db
    res['code'] = 'ok'
    res['message'] = 'create successful'
    res['ins'] = {}
    res['ins']['container_serial'] = container.get('Id')
    res['ins']['image_id'] = image_id
    res['ins']['container_name'] = kwargs.get('container_name')
    create_instance(container.get('Id'), **kwargs)
    worker_logger.info("succeed to write %s in database." % kwargs.get('container_name'))
    return json.dumps(res)

def run_container(cli, *args, **kwargs):
    res = {'code': 'error', 'message': 'problem error'}
    container_serial = kwargs['ins']['container_serial']
    response = cli.start(container=container_serial)
    if response is None:
        #update db
        inspect_res = cli.inspect_container(container_serial)
        host = inspect_res["NetworkSettings"]["IPAddress"]
        port = 22
        update_status_by_serial(container_serial, worker_cfg.RUNNING_INSTANCE)
        update_host_by_serial(container_serial, host)
        update_port_by_serial(container_serial, port)
        db_session = db.Session()
        image_query_res = db_session.query(Image).filter(Image.id == kwargs['ins']['image_id']).first()
        
        #supposed to be successful
        res['code'] = 'ok'
        res['message'] = 'create successful'
        res['ins'] = {}
        res['ins']['image_id'] = kwargs.get('image_id')
        res['ins']['image_name'] = image_query_res.image_name
        res['ins']['container_serial'] = container_serial
        res['ins']['container_name'] = kwargs['ins']['container_name']
        res['ins']['host'] = host
        res['ins']['port'] = port
        res['ins']['user_name'] = kwargs.get('user_name')
        res['ins']['status'] = worker_cfg.RUNNING_INSTANCE
        worker_logger.info("succeed to start %s." % kwargs['ins']['container_name'])     
    else:
        res['ins'] = {}
        res['ins']['container_serial'] = kwargs.get('container_serial')
        worker_logger.error("failed to start %s. %s" % (kwargs['ins']['container_name'], response))
    return json.dumps(res)

def stop_container(cli, *args, **kwargs):
    res = {'code': 'error', 'message': 'problem error'}
    response = None
    try:
        response = cli.stop(container=kwargs.get('container_serial'))
    except docker.errors.NotFound:
        res['container_serial'] = kwargs.get('container_serial')
        update_status_by_serial(kwargs.get('container_serial'), worker_cfg.FAILED_INSTANCE)
        msg = traceback.format_exc()
        msg = msg[msg.find('NotFound:'):]
        worker_logger.error("failed to stop %s. %s" % (kwargs.get('container_name'), msg))
        return json.dumps(res)

    res['code'] = 'ok'
    res['message'] = 'stop successful'
    res['container_serial'] = kwargs.get('container_serial')
    update_status_by_serial(kwargs.get('container_serial'), worker_cfg.STOP_INSTANCE)
    worker_logger.info("succeed to stop %s." % kwargs.get('container_name'))
    return json.dumps(res)

def restart_container(cli, *args, **kwargs):
    res = {'code': 'error', 'message': 'problem error'}
    response = None
    try:
        response = cli.restart(container=kwargs.get('container_serial'))
    except docker.errors.NotFound:
        res['container_serial'] = kwargs.get('container_serial')
        update_status_by_serial(kwargs.get('container_serial'), worker_cfg.FAILED_INSTANCE)
        msg = traceback.format_exc()
        msg = msg[msg.find('NotFound:'):]
        worker_logger.error("failed to restart %s. %s" % (kwargs.get('container_name'), msg))
        return json.dumps(res)

    if response is None:
        res['code'] = 'ok'
        res['message'] = 'restart successful'
        res['container_serial'] = kwargs.get('container_serial')
        update_status_by_serial(kwargs.get('container_serial'), worker_cfg.RUNNING_INSTANCE)
        worker_logger.info("succeed to restart %s." % kwargs.get('container_name'))
    return json.dumps(res)

def remove_container(cli, *args, **kwargs):
    res = {'code': 'error', 'message': 'problem error'}
    response = None
    try:
        response = cli.remove_container(container=kwargs.get('container_serial'), force=True)
    except docker.errors.NotFound:
        res['container_serial'] = kwargs.get('container_serial')
        update_status_by_serial(kwargs.get('container_serial'), worker_cfg.FAILED_INSTANCE)
        db_session = db.Session()
        instance_query_res = db_session.query(Instance).filter(Instance.container_serial == kwargs.get('container_serial')).first()
        container_name = instance_query_res.container_name
        msg = traceback.format_exc()
        msg = msg[msg.find('NotFound:'):]
        worker_logger.error("failed to remove %s. %s" % (container_name, msg))
        return json.dumps(res)

    if response is None:
        #supposed to be successful
        res['code'] = 'ok'
        res['message'] = 'remove successful'
        res['container_serial'] = kwargs.get('container_serial')

        #write db
        container_name = remove_instance(kwargs.get('container_serial'))
        worker_logger.info("succeed to remove %s." % container_name)
    return json.dumps(res)

if __name__ == '__main__':
    worker = WorkerQueue()
    worker.set_handler(worker_handler)
    worker.start_consuming()
