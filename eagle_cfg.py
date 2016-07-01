#! /usr/bin/env python
# -*- coding: utf-8 -*-

##db configuration
DB_USERNAME = 'root'
DB_PASSWORD = 'root'

DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'eagle'

##mq configuration
MQ_HOST = '172.17.0.3'
MQ_PORT = 5672
MQ_USERNAME = 'root'
MQ_PASSWORD = 'root'

##app configration
SECRET_KEY = 'development key'
SQLALCHEMY_TRACK_MODIFICATIONS = True

##log configuration
LOG_PATH = './'

##local configuration
CREATE = 1
STOP = 2
REMOVE = 3
RESTART = 4

RUNNING_INSTANCE = 1
STOP_INSTANCE = 2
FAILED_INSTANCE = 3
PENDING_INSTANCE = 4
