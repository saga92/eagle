#!/usr/bin/env python
# -*- cooding: utf-8 -*-


import unittest
import json
from base import Test
from view import *


class TestView(Test):

    def testView(self):
        response = self.app.get('/test')
        self.assertEquals(json.loads(response.data), dict(success=True))

if __name__ == '__main__':
    unittest.main()