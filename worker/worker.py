#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from utils import WorkerQueue
from utils import eagle_logger
from utils import db
from model import Instance, User
import requests
import worker_cfg

class Worker(WorkerQueue):

    def __init__(self):
        super(Worker, self).__init__()

    def run(cls, message):
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
    image_id = kwargs.get('image_id')
    image_name = worker_cfg.IMAGE_DICT.get(image_id)
    container = cli.create_container(image=image_name, detach=True, name=kwargs.get('container_name'))
    response = cli.start(container=container.get('Id'))
    if response is None:
        #supposed to be successful
        container_serial = container.get('Id')
        inspect_res = cli.inspect_container(container.get('Id'))
        host = inspect_res["NetworkSettings"]["IPAddress"]
        port = 22
        res['code'] = 'ok'
        res['message'] = 'create successful'
        res['ins'] = {}
        res['ins']['image_id'] = kwargs.get('image_id')
        res['ins']['container_serial'] = container_serial
        res['ins']['container_name'] = kwargs.get('container_name')
        res['ins']['host'] = host
        res['ins']['port'] = port
        res['ins']['user_name'] = kwargs.get('user_name')
        res['ins']['status'] = 1

        #write db
        user_query_res = db.session.query(User).filter(\
                User.username == kwargs.get('user_name')).first()
        user_id = user_query_res.id
        ins = Instance(kwargs.get('image_id'), \
                user_id, kwargs.get('container_name'), container_serial,
                host, port, 1)
        db.session.add(ins)
        db.session.commit()
        print("succeed to create %s." % kwargs.get('container_name'))
    return json.dumps(res)

def stop_container(cli, *args, **kwargs):
    res = {'code': 'error', 'message': 'problem error'}
    response = cli.stop(kwargs.get('container_serial'))
    if response is None:
        #supposed to be successful
        res['code'] = 'ok'
        res['message'] = 'stop successful'
        res['container_serial'] = kwargs.get('container_serial')

        #write db
        instance_query_res = db.session.query(Instance).filter(\
                Instance.container_serial == kwargs.get('container_serial')).first()
        instance_query_res.status = 2
        db.session.commit()
        print("succeed to stop %s." % kwargs.get('container_name'))
    return json.dumps(res)

def restart_container(cli, *args, **kwargs):
    res = {'code': 'error', 'message': 'problem error'}
    response = cli.start(container=kwargs.get('container_serial'))
    if response is None:
        res['code'] = 'ok'
        res['message'] = 'restart successful'
        res['container_serial'] = kwargs.get('container_serial')

        #write db
        instance_query_res = db.session.query(Instance).filter(\
            Instance.container_serial == kwargs.get('container_serial')).first()
        instance_query_res.status = 1
        db.session.commit()
        print("succeed to restart %s." % kwargs.get('container_name'))
    return json.dumps(res)

def remove_container(cli, *args, **kwargs):
    res = {'code': 'error', 'message': 'problem error'}
    response = cli.remove_container(container=kwargs.get('container_serial'), force=True)
    if response is None:
        #supposed to be successful
        res['code'] = 'ok'
        res['message'] = 'remove successful'
        res['container_serial'] = kwargs.get("container_serial")

        #write db
        instance_query_res = db.session.query(Instance).filter(\
                Instance.container_serial == kwargs.get('container_serial')).first()
        db.session.delete(instance_query_res)
        db.session.commit()
        print("succeed to remove %s." % kwargs.get('container_name'))
    return json.dumps(res)

if __name__ == '__main__':
    worker = Worker()
    worker.start_consuming()
