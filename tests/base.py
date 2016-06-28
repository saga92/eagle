#!/usr/bin/env python
# -*- cooding: utf-8 -*-


import unittest
from eagle import app


class Test(unittest.TestCase):


    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client();

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()