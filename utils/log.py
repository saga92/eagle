#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
import imp
import os

eagle_home = os.getenv('EAGLE_HOME', None)

if eagle_home is None:
    print('FATAL ERROR: eagle home env not set')
    exit(1)

app_conf = imp.load_source('app_conf', eagle_home + '/eagle_cfg.py')

eagle_logger = logging.getLogger('eagle')

formatter = Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
)
handler = RotatingFileHandler(app_conf.LOG_PATH + '/eagle.log', maxBytes=10000000, backupCount=2)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

eagle_logger.addHandler(handler)

if __name__ == '__main__':
    eagle_logger.error('test')
