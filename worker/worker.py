#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from utils import MessageQueue
from utils import eagle_logger
import requests
import worker_cfg

class Client(MessageQueue):
    @classmethod
    def process_message(cls, message_body):
        policy = json.loads(message_body)
        cli = connect_docker_cli()
        if policy['operate'] == worker_cfg.CREATE_INSTANCE:
            create_run_container(cli, **policy)

def connect_docker_cli():
    from docker import Client
    cli = Client(base_url=worker_cfg.DOCKER_CLI_URL)
    return cli

def create_run_container(cli, *args, **kwargs):
    image_id = kwargs.get('image_id')
    image_name = worker_cfg.IMAGE_DICT.get(image_id)
    container = cli.create_container(image=image_name, detach=True, name=kwargs.get('container_name'))
    response = cli.start(container=container.get('Id'))
    if response is None:
        #supposed to be successful
        inspect_res = cli.inspect_container(container.get('Id'))
        policy_res = {}
        policy_res['image_id'] = kwargs.get('image_id')
        policy_res['container_serial'] = container.get('Id')
        policy_res['container_name'] = kwargs.get('container_name')
        policy_res['host'] = inspect_res["NetworkSettings"]["IPAddress"]
        policy_res['port'] = 22
        policy_res['user_name'] = kwargs.get('user_name')
        policy_res['status'] = 1
        ui_response = requests.post(worker_cfg.UI_HOST + '/create_ins_res', data=policy_res)
        print("succeed to create %s." % kwargs.get('container_name'))

if __name__ == '__main__':
    Client.connect()
    Client.start_consuming()
    Client.disconnect()
