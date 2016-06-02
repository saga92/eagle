#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from utils import MessageQueue
import requests

image_dict = {'1': 'eagle-ubuntu:latest'}

class Client(MessageQueue):
    @classmethod
    def process_message(cls, message_body):
        policy = json.loads(message_body)
        cli = connect_docker_cli()
        run_container(cli, **policy)

def connect_docker_cli():
    from docker import Client
    cli = Client(base_url='unix://var/run/docker.sock')
    return cli

def run_container(cli, *args, **kwargs):
    image_id = kwargs.get('image_id')
    image_name = image_dict.get(image_id)
    container = cli.create_container(image=image_name, detach=True, name=kwargs.get('container_name'))
    response = cli.start(container=container.get('Id'))
    if response is None:
        #supposed to be successful
        policy_res = {}
        policy_res['image_id'] = kwargs.get('image_id')
        policy_res['container_serial'] = container.get('Id')
        policy_res['container_name'] = kwargs.get('container_name')
        policy_res['user_name'] = kwargs.get('user_name')
        policy_res['status'] = 1
        ui_response = requests.post('http://10.117.171.162:8088/update_ins', data=policy_res)

if __name__ == '__main__':
    Client.connect()
    Client.start_consuming()
    Client.disconnect()
