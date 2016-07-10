#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

eagle_home = os.getenv('EAGLE_HOME', None)

if eagle_home is None:
    print('FATAL ERROR: eagle home env not set')
    exit(1)

from log import eagle_logger, worker_logger, ui_logger
from mq import UiQueue, WorkerQueue
