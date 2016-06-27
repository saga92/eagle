#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import db
from model import Instance

def updateDB(res, status, **kwargs):
    db_session = db.Session()
    res['container_serial'] = kwargs.get('container_serial')
    instance_query_res = db_session.query(Instance).filter(Instance.container_serial == kwargs.get('container_serial')).first()
    instance_query_res.status = status
    db_session.commit()
