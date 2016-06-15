#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__, template_folder='public', static_folder='public')
app.config.from_pyfile('eagle_cfg.py')

