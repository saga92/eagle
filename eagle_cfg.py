#! /usr/bin/env python
# -*- coding: utf-8 -*-

##db configuration
DB_USERNAME = 'root'
DB_PASSWORD = 'root123'
DB_HOST = '192.168.99.100'
DB_PORT = '3306'
DB_NAME = 'eagle'

##mq configuration
MQ_HOST = '192.168.99.100'
MQ_PORT = 8084
MQ_USERNAME = 'root'
MQ_PASSWORD = 'root'

##app configration
SECRET_KEY = 'development key'
SQLALCHEMY_TRACK_MODIFICATIONS = True

##log configuration
LOG_PATH = '/Users/heyahao/project/pyproject/eagle'

##local configuration
CREATE_INSTANCE = 1
STOP_INSTANCE = 2
REMOVE_INSTANCE = 3
