#!/usr/bin/env python
# -*- cooding: utf-8 -*-
# flake8: noqa

import unittest
import json

from base import UnitTest
from tests import test_cfg
from dao import *
from view.user import *
from eagle import app

import copy

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

    #Test modify profile
    def test_modify_profile(self):
        create_user(self.user)
        db_session = db.Session()
        user_query_res = db_session.query(User).filter(User.username == test_cfg.USER_NAME).first()
        req = dict(
            id=user_query_res.id,
            username='test'+test_cfg.USER_NAME,
            password='test'+test_cfg.USER_PASSWORD,
            email='test'+test_cfg.USER_EMAIL
        )
        response = self.app.post('/profile', data=json.dumps(req), follow_redirects=True)
        remove_user_by_id(user_query_res.id)
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x1')

    # Username occupied
    def test_modify_username_failed(self):
        create_user(self.user)
        another_user = copy.deepcopy(self.user)
        another_user['username'] = 'test'+test_cfg.USER_NAME
        create_user(another_user)
        db_session = db.Session()
        user_query_res = db_session.query(User).filter(User.username == test_cfg.USER_NAME).first()
        req = dict(
            id=user_query_res.id,
            username='test'+test_cfg.USER_NAME,
            password=test_cfg.USER_PASSWORD,
            email=test_cfg.USER_EMAIL
        )
        response = self.app.post('/profile', data=json.dumps(req), follow_redirects=True)
        remove_user_by_id(user_query_res.id)
        remove_user_by_username(another_user['username'])
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x4')

    # Email occupied
    def test_modify_email_failed(self):
        create_user(self.user)
        another_user = copy.deepcopy(self.user)
        another_user['username'] = 'test'+test_cfg.USER_NAME
        another_user['email'] = 'test'+test_cfg.USER_EMAIL
        create_user(another_user)
        db_session = db.Session()
        user_query_res = db_session.query(User).filter(User.username == test_cfg.USER_NAME).first()
        req = dict(
            id=user_query_res.id,
            username=test_cfg.USER_NAME,
            password=test_cfg.USER_PASSWORD,
            email='test'+test_cfg.USER_EMAIL
        )
        response = self.app.post('/profile', data=json.dumps(req), follow_redirects=True)
        remove_user_by_id(user_query_res.id)
        remove_user_by_username(another_user['username'])
        res_dict = json.loads(response.data)
        self.assertEquals(res_dict.get('code'), '0x5')

if __name__ == '__main__':
    unittest.main()
