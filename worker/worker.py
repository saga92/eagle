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
from dao import update_status_by_serial

def worker_handler(message):
    res = None
    policy = json.loads(message)
    cli = connect_docker_cli()
    if policy['operate'] == worker_cfg.CREATE_INSTANCE:
        res = create_run_container(cli, **policy)
    elif policy['operate'] == worker_cfg.STOP_INSTANCE:
        res = stop_container(cli, **policy)
    elif policy['operate'] == worker_cfg.RESTART_INSTANCE:
        res = restart_container(cli, **policy)
    elif policy['operate'] == worker_cfg.REMOVE_INSTANCE:
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
    res = {'code': 'error', 'message': 'problem error'}
    container = create_container(cli, *args, **kwargs)
    if (container == None):
        res['ins'] = {}
        worker_logger.info("failed to create %s, create_container() crashed with APIError." % kwargs.get('container_name'))
        return json.dumps(res)
    else:
        worker_logger.info("succeed to write %s in database." % kwargs.get('container_name'))

    ret = run_container(cli, container, *args, **kwargs)
    if (ret == None):
        res['ins'] = {}
        worker_logger.info("failed to start %s." % kwargs.get('container_name'))
        return json.dumps(res)
    else:
        worker_logger.info("succeed to start %s." % kwargs.get('container_name'))
        return ret

def create_container(cli, *args, **kwargs):
    image_id = kwargs.get('image_id')
    image_name = worker_cfg.IMAGE_DICT.get(image_id)
    try:
        container = cli.create_container(image=image_name, detach=True, name=kwargs.get('container_name'))
    except docker.errors.APIError:
        return None

    container_serial = container.get('Id')
    inspect_res = cli.inspect_container(container.get('Id')) #inspect_res is validate after container start
    host = inspect_res["NetworkSettings"]["IPAddress"]
    port = 22

    #write db
    db_session = db.Session()
    user_query_res = db_session.query(User).filter(User.username == kwargs.get('user_name')).first()
    user_id = user_query_res.id
    ins = Instance(kwargs.get('image_id'), \
                   user_id, kwargs.get('container_name'), container_serial,
                   host, port, 6)
    db_session.add(ins)
    db_session.commit()
    return container

def run_container(cli, container, *args, **kwargs):
    res = {'code': 'error', 'message': 'problem error'}
    response = cli.start(container=container.get('Id'))
    if response is None:
        #update db
        db_session = db.Session()
        container_serial = container.get('Id')
        instance_query_res = db_session.query(Instance).filter(Instance.container_serial == container_serial).first()
        inspect_res = cli.inspect_container(container.get('Id'))
        host = inspect_res["NetworkSettings"]["IPAddress"]
        port = 22
        instance_query_res.host = host
        instance_query_res.status = 1
        db_session.commit()
        image_query_res = db_session.query(Image).filter(Image.id == kwargs.get('image_id')).first()
        
        #supposed to be successful
        res['code'] = 'ok'
        res['message'] = 'create successful'
        res['ins'] = {}
        res['ins']['image_id'] = kwargs.get('image_id')
        res['ins']['image_name'] = image_query_res.image_name
        res['ins']['container_serial'] = container_serial
        res['ins']['container_name'] = kwargs.get('container_name')
        res['ins']['host'] = host
        res['ins']['port'] = port
        res['ins']['user_name'] = kwargs.get('user_name')
        res['ins']['status'] = 1

        return json.dumps(res)
    else:
        res['container_serial'] = kwargs.get('container_serial')
        return json.dumps(res)

def stop_container(cli, *args, **kwargs):
    res = {'code': 'error', 'message': 'problem error'}
    response = None
    try:
        response = cli.stop(kwargs.get('container_serial'))
    except docker.errors.NotFound:
        res['container_serial'] = kwargs.get('container_serial')
        update_status_by_serial(5, kwargs.get('container_serial'))
        worker_logger.info("failed to stop %s. stop() crashed with NotFound" % kwargs.get('container_name'))
        return json.dumps(res)

    res['code'] = 'ok'
    res['message'] = 'stop successful'
    res['container_serial'] = kwargs.get('container_serial')
    update_status_by_serial(2, kwargs.get('container_serial'))
    worker_logger.info("succeed to stop %s." % kwargs.get('container_name'))
    return json.dumps(res)

def restart_container(cli, *args, **kwargs):
    res = {'code': 'error', 'message': 'problem error'}
    response = None
    try:
        response = cli.start(container=kwargs.get('container_serial'))
    except docker.errors.NotFound:
        res['container_serial'] = kwargs.get('container_serial')
        update_status_by_serial(5, kwargs.get('container_serial'))
        worker_logger.info("failed to restart %s. restart() crashed with NotFound" % kwargs.get('container_name'))
        return json.dumps(res)

    if response is None:
        res['code'] = 'ok'
        res['message'] = 'restart successful'
        res['container_serial'] = kwargs.get('container_serial')
        update_status_by_serial(1, kwargs.get('container_serial'))
        worker_logger.info("succeed to restart %s." % kwargs.get('container_name'))
    return json.dumps(res)

def remove_container(cli, *args, **kwargs):
    res = {'code': 'error', 'message': 'problem error'}
    response = None
    try:
        response = cli.remove_container(container=kwargs.get('container_serial'), force=True)
    except docker.errors.NotFound:
        res['container_serial'] = kwargs.get('container_serial')
        update_status_by_serial(5, kwargs.get('container_serial'))
        worker_logger.info("failed to remove %s. remove() crashed with NotFound" % kwargs.get('container_name'))
        return json.dump(res)

    if response is None:
        #supposed to be successful
        res['code'] = 'ok'
        res['message'] = 'remove successful'
        res['container_serial'] = kwargs.get("container_serial")

        #write db
        db_session = db.Session()
        instance_query_res = db_session.query(Instance).filter(\
                Instance.container_serial == kwargs.get('container_serial')).first()
        container_name = instance_query_res.container_name
        db_session.delete(instance_query_res)
        db_session.commit()
        worker_logger.info("succeed to remove %s." % container_name)
    return json.dumps(res)

if __name__ == '__main__':
    worker = WorkerQueue()
    worker.set_handler(worker_handler)
    worker.start_consuming()
