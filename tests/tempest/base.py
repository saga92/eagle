#!/usr/bin/env python
# -*- cooding: utf-8 -*-


import random
import string
import unittest

from eagle import app
from utils import eagle_logger



class Test(unittest.TestCase):

    def setUp(self):
        eagle_logger.disabled = True
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def get_random_string(self, n = 5):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))

if __name__ == '__main__':
    unittest.main()
