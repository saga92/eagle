#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import db
from model import Instance

def update_status_by_serial(status, container_serial):
    db_session = db.Session()
    instance_query_res = db_session.query(Instance).filter(Instance.container_serial == container_serial).first()
    instance_query_res.status = status
    db_session.commit()
