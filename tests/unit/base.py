#!/usr/bin/env python
# -*- cooding: utf-8 -*-

import random
import string
import unittest
import os

from utils import eagle_logger, ui_logger, worker_logger


class UnitTest(unittest.TestCase):

    def setUp(self):
        eagle_logger.disabled = True
        ui_logger.disabled = True
        worker_logger.disabled = True

    # Clear the log file
    def tearDown(self):
        files = os.listdir(os.getcwd())
        for f in files:
            if f.endswith(".log"):
                os.remove(f)

    def get_random_string(self, n = 5):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))

if __name__ == '__main__':
    unittest.main()
