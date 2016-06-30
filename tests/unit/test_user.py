#!/usr/bin/env python
#! -*- coding: utf-8 -*-

import mock
import unittest
from view import user
from view import request
from base import UnitTest


class TestUser(UnitTest):

    def test_1_siginup_success(self):
        req = dict(
            username=test_cfg.USER_NAME_TEST,
            email=test_cfg.USER_EMAIL_TEST,
            password=test_cfg.USER_PASSWORD_TEST
        )
        response = self.app.post('/signup', data=json.dumps(req), follow_redirects=True)
if __name__ == '__main__':
    unittest.main()