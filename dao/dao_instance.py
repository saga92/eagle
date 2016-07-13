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

from utils import db
from model import Instance

def update_instance_by_serial(container_serial, **kwargs):
    db_session = db.Session()
    instance_query_res = db_session.query(Instance).filter(\
            Instance.container_serial == container_serial).first()
    for key in kwargs:
        setattr(instance_query_res, key, kwargs.get(key))
    db_session.commit()

def update_status_by_serial(container_serial, status):
    update_instance_by_serial(container_serial, status=status)

def update_host_by_serial(container_serial, host):
    update_instance_by_serial(container_serial, host=host)

def update_port_by_serial(container_serial, port):
    update_instance_by_serial(container_serial, port=port)

def create_instance(ins):
    db_session = db.Session()
    ins = Instance(ins.get('image_id'),\
            ins.get('user_id'), ins.get('container_name'),\
            ins.get('container_serial'), ins.get('host'), \
            ins.get('port'), ins.get('status'), ins.get('jump_server'))
    db_session.add(ins)
    db_session.commit()

def remove_instance_by_serial(container_serial):
    db_session = db.Session()
    instance_query_res = db_session.query(Instance).filter(Instance.container_serial == container_serial).first()
    container_name = instance_query_res.container_name
    db_session.delete(instance_query_res)
    db_session.commit()
    return container_name

def get_instance_by_serial(container_serial):
    db_session = db.Session()
    instance_query_res = db_session.query(Instance).filter(Instance.container_serial == container_serial).first()
    return instance_query_res
