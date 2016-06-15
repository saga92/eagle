#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import imp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app_conf = imp.load_source('app_conf', os.getenv('EAGLE_HOME', '..') + '/eagle_cfg.py')

SQLALCHEMY_DATABASE_URI =\
    'mysql://'+app_conf.DB_USERNAME + ':' + \
    app_conf.DB_PASSWORD + '@' + app_conf.DB_HOST + \
    ':'+app_conf.DB_PORT + '/' + app_conf.DB_NAME

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

session = Session()

if __name__ == '__main__':
    user1 = session.query(User).first()
    print user1.password
