#!/usr/bin/env python
# -*- cooding: utf-8 -*-

import unittest

from base import Test
from tests import test_cfg
from tests.test_util import *
from view import *


class TestUser(Test):


    def test_1_signup_success(self):
        req = dict(
            username=test_cfg.USER_NAME_TEST,
            email=test_cfg.USER_EMAIL_TEST,
            password=test_cfg.USER_PASSWORD_TEST
        )
        response = self.app.post('/signup', data=json.dumps(req), follow_redirects=True)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x1')

    # Email address is occupied by others
    def test_2_signup_email_failed(self):
        req = dict(
            username=self.get_random_string(),
            email=test_cfg.USER_EMAIL_TEST,
            password=test_cfg.USER_PASSWORD_TEST
        )
        response = self.app.post('/signup', data=json.dumps(req), follow_redirects=True)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x5')

    # User name is occupied by others
    def test_3_signup_name_failed(self):
        req = dict(
            username=test_cfg.USER_NAME_TEST,
            email=self.get_random_string(),
            password=test_cfg.USER_PASSWORD_TEST
        )
        response = self.app.post('/signup', data=json.dumps(req), follow_redirects=True)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x4')

    # Test sigin with user name
    def test_4_signin_with_name_success(self):
        req = dict(
            username=test_cfg.USER_NAME_TEST,
            password=test_cfg.USER_PASSWORD_TEST
        )
        response = self.app.post('/signin', data=json.dumps(req), follow_redirects=True)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x1')

    # Test sigin in with email
    def test_5_signin_with_email_success(self):
        req = dict(
            username=test_cfg.USER_EMAIL_TEST,
            password=test_cfg.USER_PASSWORD_TEST
        )
        response = self.app.post('/signin', data=json.dumps(req), follow_redirects=True)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x1')

    # User name doesn't exist
    def test_6_signin_name_failed(self):
        req = dict(
            username=self.get_random_string(),
            password=test_cfg.USER_PASSWORD_TEST
        )
        response = self.app.post('/signin', data=json.dumps(req), follow_redirects=True)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x7')

    # Password is wrong
    def test_7_sigin_password_failed(self):
        req = dict(
            username=test_cfg.USER_NAME_TEST,
            password=self.get_random_string()
        )
        response = self.app.post('/signin', data=json.dumps(req), follow_redirects=True)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x6')

    def test_8_signout(self):
        response = self.app.get('/signout', follow_redirects=True)
        self.assertEquals(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
