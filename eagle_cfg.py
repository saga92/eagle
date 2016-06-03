#! /usr/bin/env python
# -*- coding: utf-8 -*-

##db configuration
DB_USERNAME = 'root'
DB_PASSWORD = 'root123'
DB_HOST = '172.18.0.4'
DB_PORT = '3306'
DB_NAME = 'eagle'

##mq configuration
MQ_HOST = '172.17.0.2'
MQ_PORT = 5672
MQ_USERNAME = 'root'
MQ_PASSWORD = 'root'

##app configration
SECRET_KEY = 'development key'
SQLALCHEMY_TRACK_MODIFICATIONS = True

##log configuration
LOG_PATH = '/root/proj/eagle'

##local configuration
CREATE_INSTANCE = 1
