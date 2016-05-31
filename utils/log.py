#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from eagle import app

formatter = Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
)
handler = RotatingFileHandler(app.config['LOG_FILENAME'], maxBytes=10000000, backupCount=2)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
logger = app.logger

if __name__ == '__main__':
    app.logger.error('test')
