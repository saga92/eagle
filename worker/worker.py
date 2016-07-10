# Copyright (c) the Eagle authors and contributors.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from utils import WorkerQueue
from utils import worker_logger
from utils import db
from model import Instance, User, Image
import worker_cfg
from dao import *
import docker

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
    cli = docker.Client(base_url=worker_cfg.DOCKER_CLI_URL)
    return cli

def create_container(cli, *args, **kwargs):
    res = {'code': '0x2', 'message': 'Unknown problem', 'ins': {}}
    image_id = kwargs.get('image_id')
    image_name = worker_cfg.IMAGE_DICT.get(image_id)
    db_session = db.Session()
    user_query_res = db_session.query(User).filter(\
            User.username == kwargs.get('user_name')).first()
    user_id = user_query_res.id
    try:
        container = cli.create_container(image=image_name, detach=True, name=kwargs.get('container_name'))
    except docker.errors.APIError as e:
        msg = str(e)
        res['code'] = '0x3'
        res['message'] = msg
        res['ins']['container_serial'] = ''
        res['ins']['image_id'] = image_id
        res['ins']['user_id'] = user_id
        res['ins']['host'] = ''
        res['ins']['port'] = 0
        res['ins']['jump_server'] = ''
        res['ins']['container_name'] = kwargs.get('container_name')
        res['ins']['image_name'] = image_name
        res['ins']['status'] = worker_cfg.FAILED_INSTANCE
        worker_logger.error("failed to create %s. %s" % (kwargs.get('container_name'), msg))
    else:
        #write db
        res['code'] = '0x1'
        res['message'] = 'create successful'
        res['ins']['container_serial'] = container.get('Id')
        res['ins']['image_id'] = image_id
        res['ins']['user_id'] = user_id
        res['ins']['host'] = ''
        res['ins']['port'] = 0
        res['ins']['container_name'] = kwargs.get('container_name')
        res['ins']['image_name'] = image_name
        res['ins']['status'] = worker_cfg.STOP_INSTANCE
        res['ins']['jump_server'] = worker_cfg.DEPLOY_HOSTNAME
        worker_logger.info("succeed to write %s in database." % kwargs.get('container_name'))
    create_instance(res['ins'])
    return json.dumps(res)

def run_container(cli, *args, **kwargs):
    res = {'code': '0x2', 'message': 'Unknown problem', 'ins': {}}
    container_serial = kwargs.get('container_serial')
    response = cli.start(container=container_serial)
    if response is None:
        #update db
        inspect_res = cli.inspect_container(container_serial)
        host = inspect_res["NetworkSettings"]["IPAddress"]
        port = 22
        update_instance(container_serial, status=worker_cfg.RUNNING_INSTANCE,\
                host=host, port=port)
        db_session = db.Session()
        image_query_res = db_session.query(Image).filter(\
                Image.id == kwargs.get('image_id')).first()
        res['code'] = '0x1'
        res['message'] = 'running successful'
        res['ins']['image_id'] = kwargs.get('image_id')
        res['ins']['image_name'] = image_query_res.image_name
        res['ins']['container_serial'] = container_serial
        res['ins']['container_name'] = kwargs.get('container_name')
        res['ins']['host'] = host
        res['ins']['port'] = port
        res['ins']['user_name'] = kwargs.get('user_name')
        res['ins']['status'] = worker_cfg.RUNNING_INSTANCE
        res['ins']['jump_server'] = worker_cfg.DEPLOY_HOSTNAME
        worker_logger.info("succeed to start %s." % kwargs.get('container_name'))
    else:
        res['ins']['container_serial'] = kwargs.get('container_serial')
        worker_logger.error("failed to start %s. %s" % (kwargs.get('container_name'), response))
    return json.dumps(res)

def create_run_container(cli, *args, **kwargs):
    res = create_container(cli, **kwargs)
    res_dict = json.loads(res)
    if (res_dict['code'] == '0x1'):
        res = run_container(cli, **res_dict['ins'])
    return res

def stop_container(cli, *args, **kwargs):
    res = {'code': '0x2', 'message': 'Unknown problem', 'container_serial': ''}
    response = None
    try:
        response = cli.stop(container=kwargs.get('container_serial'))
    except docker.errors.NotFound as e:
        res['container_serial'] = kwargs.get('container_serial')
        update_status_by_serial(kwargs.get('container_serial'), worker_cfg.FAILED_INSTANCE)
        msg = str(e)
        res['message'] = msg
        worker_logger.error("failed to stop %s. %s" % (kwargs.get('container_name'), msg))
    else:
        res['code'] = '0x1'
        res['message'] = 'stop successful'
        res['container_serial'] = kwargs.get('container_serial')
        update_instance(kwargs.get('container_serial'), status=worker_cfg.STOP_INSTANCE,\
                host='', port=0)
        worker_logger.info("succeed to stop %s." % kwargs.get('container_name'))
    return json.dumps(res)

def restart_container(cli, *args, **kwargs):
    res = {'code': '0x2', 'message': 'Unknown problem', 'container_serial': ''}
    response = None
    try:
        response = cli.restart(container=kwargs.get('container_serial'))
    except docker.errors.NotFound as e:
        res['container_serial'] = kwargs.get('container_serial')
        update_status_by_serial(kwargs.get('container_serial'), worker_cfg.FAILED_INSTANCE)
        msg = str(e)
        res['message'] = msg
        worker_logger.error("failed to restart %s. %s" % (kwargs.get('container_name'), msg))
    else:
        if response is None:
            res['code'] = '0x1'
            res['message'] = 'restart successful'
            res['container_serial'] = kwargs.get('container_serial')
            inspect_res = cli.inspect_container(kwargs.get('container_serial'))
            host = inspect_res["NetworkSettings"]["IPAddress"]
            port = 22
            res['host'] = host
            res['port'] = port
            update_instance(kwargs.get('container_serial'), status=worker_cfg.RUNNING_INSTANCE,\
                    host=host, port=port)
            worker_logger.info("succeed to restart %s." % kwargs.get('container_name'))
        else:
            res['container_serial'] = kwargs.get('container_serial')
            worker_logger.error("failed to restart %s. %s" % (kwargs.get('container_name'), response))
    return json.dumps(res)

def remove_container(cli, *args, **kwargs):
    res = {'code': '0x2', 'message': 'Unknown problem', 'container_serial': ''}
    response = None
    try:
        response = cli.remove_container(container=kwargs.get('container_serial'), force=True)
    except docker.errors.NotFound as e:
        res['container_serial'] = kwargs.get('container_serial')
        update_status_by_serial(kwargs.get('container_serial'), worker_cfg.FAILED_INSTANCE)
        msg = str(e)
        res['message'] = msg
        worker_logger.error("failed to remove %s. %s" % (kwargs.get('container_name'), msg))
    else:
        if response is None:
            #supposed to be successful
            res['code'] = '0x1'
            res['message'] = 'remove successful'
            res['container_serial'] = kwargs.get('container_serial')

            #write db
            container_name = remove_instance_by_serial(kwargs.get('container_serial'))
            worker_logger.info("succeed to remove %s." % container_name)
        else:
            res['container_serial'] = kwargs.get('container_serial')
            worker_logger.error("failed to restart %s. %s" % (kwargs.get('container_name'), response))
    return json.dumps(res)

if __name__ == '__main__':
    worker = WorkerQueue()
    worker.set_handler(worker_handler)
    worker.start_consuming()
