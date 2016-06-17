#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler
from logging import Formatter
import imp
import os
import sys
import time

eagle_logger = None
ui_logger = None
worker_logger = None

def get_logger(logger_name):
    app_conf = imp.load_source('app_conf', os.getenv('EAGLE_HOME', '..') + '/eagle_cfg.py')

    _logger = logging.getLogger(logger_name)

    file_formatter = Formatter(
        '%(levelname)s | %(asctime)s | %(name)s | %(message)s | %(pathname)s:%(lineno)d'
    )
    time_rotating_handler = TimedRotatingFileHandler(\
            '{0}/{1}.log'.format(app_conf.LOG_PATH, logger_name), when="midnight", encoding='utf-8')
    time_rotating_handler.suffix = "%Y-%m-%d"
    time_rotating_handler.setFormatter(file_formatter)

    stream_handler = StreamHandler(stream=sys.stdout)
    echo_formatter = Formatter('[%(levelname)s][%(name)s][in %(filename)s:%(lineno)d] %(message)s')
    stream_handler.setFormatter(echo_formatter)

    _logger.addHandler(time_rotating_handler)
    _logger.addHandler(stream_handler)
    _logger.setLevel(logging.DEBUG)

    return _logger

if eagle_logger is None:
    eagle_logger = get_logger('eagle')

if ui_logger is None:
    ui_logger = get_logger('ui')

if worker_logger is None:
    worker_logger = get_logger('worker')

if __name__ == '__main__':
    eagle_logger.debug('this is a log for test reason')
