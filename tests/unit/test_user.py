#!/usr/bin/env python
# -*- cooding: utf-8 -*-

import unittest
import json

from base import UnitTest
from tests import test_cfg
from dao import *
from view.user import *
from eagle import app


class TestUser(UnitTest):

    def setUp(self):
        super(TestUser, self).setUp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.user = dict(
            username=test_cfg.USER_NAME,
            email=test_cfg.USER_EMAIL,
            password=test_cfg.USER_PASSWORD
        )

    def test_signup_success(self):
        req = dict(
            username=test_cfg.USER_NAME,
            email=test_cfg.USER_EMAIL,
            password=test_cfg.USER_PASSWORD
        )
        response = self.app.post('/signup', data=json.dumps(req), follow_redirects=True)
        remove_user_by_username(test_cfg.USER_NAME)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x1')

    # Email address is occupied by others
    def test_signup_email_failed(self):
        create_user(self.user)
        req = dict(
            username=self.get_random_string(),
            email=test_cfg.USER_EMAIL,
            password=test_cfg.USER_PASSWORD
        )
        response = self.app.post('/signup', data=json.dumps(req), follow_redirects=True)
        remove_user_by_username(test_cfg.USER_NAME)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x5')

    # User name is occupied by others
    def test_signup_name_failed(self):
        create_user(self.user)
        req = dict(
            username=test_cfg.USER_NAME,
            email=self.get_random_string(),
            password=test_cfg.USER_PASSWORD
        )
        response = self.app.post('/signup', data=json.dumps(req), follow_redirects=True)
        remove_user_by_username(test_cfg.USER_NAME)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x4')

    # Test sigin with user name
    def test_signin_with_name_success(self):
        create_user(self.user)
        req = dict(
            username=test_cfg.USER_NAME,
            password=test_cfg.USER_PASSWORD
        )
        response = self.app.post('/signin', data=json.dumps(req), follow_redirects=True)
        remove_user_by_username(test_cfg.USER_NAME)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x1')

    # Test sigin in with email
    def test_signin_with_email_success(self):
        create_user(self.user)
        req = dict(
            username=test_cfg.USER_EMAIL,
            password=test_cfg.USER_PASSWORD
        )
        response = self.app.post('/signin', data=json.dumps(req), follow_redirects=True)
        remove_user_by_username(test_cfg.USER_NAME)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x1')

    # User name doesn't exist
    def test_signin_name_failed(self):
        req = dict(
            username=self.get_random_string(),
            password=test_cfg.USER_PASSWORD
        )
        response = self.app.post('/signin', data=json.dumps(req), follow_redirects=True)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x7')

    # Password is wrong
    def test_sigin_password_failed(self):
        create_user(self.user)
        req = dict(
            username=test_cfg.USER_NAME,
            password=self.get_random_string()
        )
        response = self.app.post('/signin', data=json.dumps(req), follow_redirects=True)
        remove_user_by_username(test_cfg.USER_NAME)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x6')

    def test_signout(self):
        response = self.app.get('/signout', follow_redirects=True)
        self.assertEquals(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
