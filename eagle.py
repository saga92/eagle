#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('eagle.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'mysql://'+app.config['DB_USERNAME'] + ':' + \
    app.config['DB_PASSWORD']+'@' + app.config['DB_HOST'] + \
    ':'+app.config['DB_PORT']+'/'+app.config['DB_NAME']

db = SQLAlchemy(app)

