#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
import imp
import os

app_conf = imp.load_source('app_conf', os.getenv('EAGLE_HOME', '..') + '/eagle_cfg.py')

eagle_logger = logging.getLogger('eagle')

formatter = Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
)
handler = RotatingFileHandler(app_conf.LOG_PATH + '/eagle.log', maxBytes=10000000, backupCount=2)
handler.setFormatter(formatter)

eagle_logger.addHandler(handler)
eagle_logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    eagle_logger.debug('this is a log for test reason')
