#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
import imp
import os

eagle_home = os.getenv('EAGLE_HOME', None)

app_conf = imp.load_source('app_conf', eagle_home + '/eagle.cfg')

eagle_logger = logging.getLogger('eagle')

formatter = Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
)
handler = RotatingFileHandler(app_conf.EAGLE_PATH + '/' + app_conf.LOG_FILENAME, maxBytes=10000000, backupCount=2)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

eagle_logger.addHandler(handler)

if __name__ == '__main__':
    eagle_logger.error('test')
