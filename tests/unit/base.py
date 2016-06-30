#!/usr/bin/env python
#! -*- coding: utf-8 -*-

import unittest
import mock
from tests import test_cfg
from model import User, Instance
from view import request
from eagle import app


class UnitTest(unittest.TestCase):


    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def get_random_string(self, n=5):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))

    def clear_users(self):

        # Delete the user generated in test
        db_session = db.Session()
        user_res = db_session.query(User).filter(or_(User.username == \
                                                     test_cfg.USER_NAME_TEST, User.email == test_cfg.USER_EMAIL_TEST))
        if user_res is not None:
            for user in user_res:
                db_session.delete(user)
                db_session.commit()

    def clear_instances(self):

        # Remove the docker container
        container_serial = self.get_container_serial_by_name(test_cfg.INSTANCE_NAME_TEST)
        if container_serial is not None:
            req = dict(
                container_serial=container_serial,
                user_name=test_cfg.USER_NAME_TEST
            )
            self.app.post('/remove_ins', data=json.dumps(req), follow_redirects=True)

        # Delete the instance generated in test
        db_session = db.Session()
        instance_res = db_session.query(Instance).filter(Instance.container_name == \
                                                         test_cfg.INSTANCE_NAME_TEST)
        if instance_res is not None:
            for instance in instance_res:
                db_session.delete(instance)
                db_session.commit()

    def clear_log_file(self):
        files = os.listdir(os.getcwd())
        for f in files:
            if f.endswith(".log"):
                os.remove(f)

    def get_container_serial_by_name(self, container_name):
        db_session = db.Session()
        instance_res = db_session.query(Instance).filter(Instance.container_name == \
                                                         test_cfg.INSTANCE_NAME_TEST).first()
        if instance_res is not None:
            return instance_res.container_serial
        else:
            return None
