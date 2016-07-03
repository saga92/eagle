#!/usr/bin/env python
# -*- cooding: utf-8 -*-

import unittest
import mock
import json

from base import UnitTest
from tests import test_cfg
from utils import UiQueue
from view.instance import *
from eagle import app
from dao import *

container_serial = None

class TestInstance(UnitTest):

    def setUp(self):
        super(TestInstance, self).setUp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.ins = dict(
            image_id=test_cfg.CONTAINER_IMAGE_ID,
            user_id=1,
            container_name=test_cfg.CONTAINER_NAME,
            container_serial=test_cfg.CONTAINER_SERIAL,
            host='10.0.0.1',
            port=22,
            status=1,
            jump_server='127.0.0.1'
        )

    def test_list(self):
        create_user(dict(
            username=test_cfg.USER_NAME,
            email=test_cfg.USER_EMAIL,
            password=test_cfg.USER_PASSWORD
        ))
        user = get_user_by_username(test_cfg.USER_NAME)
        user_id = user.id
        self.ins.update({'user_id':user_id})
        create_instance(self.ins)
        response = self.app.get('/list_ins?signin_username=' + test_cfg.USER_NAME,
                                follow_redirects=True)
        remove_user_by_username(test_cfg.USER_NAME)
        remove_instance_by_serial(self.ins['container_serial'])
        res_dict = json.loads(response.data)
        self.assertEqual(res_dict.get('code'), '0x1')
        self.assertEqual(len(res_dict.get('instances')), 1)

    def test_create_success(self):
        req = dict(
            container_name=test_cfg.CONTAINER_NAME,
            image_id=test_cfg.CONTAINER_IMAGE_ID,
            user_name=test_cfg.USER_NAME
        )
        with mock.patch.object(UiQueue, 'send'
                               ) as mock_queue_send:
            worker_res = dict(
                code='0x1',
                message='pass',
                ins={}
            )
            mock_queue_send.return_value = json.dumps(worker_res)
            response = self.app.post('/create_ins', data = json.dumps(req), follow_redirects=True)
            mock_queue_send.assert_called_once()
            res_dict = json.loads(response.data)
            self.assertEqual(res_dict.get('code'), '0x1')

    # Container name occupied by others
    def test_create_failed(self):
        create_instance(self.ins)
        req = dict(
            container_name=test_cfg.CONTAINER_NAME,
            image_id=test_cfg.CONTAINER_IMAGE_ID,
            user_name=test_cfg.USER_NAME
        )
        with mock.patch.object(UiQueue, 'send'
                               ) as mock_queue_send:
            worker_res = dict(
                code='0x1',
                message='pass',
                ins={}
            )
            mock_queue_send.return_value = json.dumps(worker_res)
            response = self.app.post('/create_ins', data = json.dumps(req), follow_redirects=True)
            remove_instance_by_serial(self.ins.get('container_serial'))
            res_dict = json.loads(response.data)
            self.assertEqual(res_dict.get('code'), '0x8')

    def test_stop_success(self):
        create_instance(self.ins)
        req = dict(
            container_serial=self.ins.get('container_serial'),
            user_name=test_cfg.USER_NAME
        )
        with mock.patch.object(UiQueue, 'send'
                               ) as mock_queue_send:
            worker_res = dict(
                code='0x1',
                message='pass',
                container_serial=self.ins.get('container_serial')
            )
            mock_queue_send.return_value = json.dumps(worker_res)
            response = self.app.post('/stop_ins', data=json.dumps(req), follow_redirects=True)
            remove_instance_by_serial(self.ins.get('container_serial'))
            mock_queue_send.assert_called_once()
            res_dict = json.loads(response.data)
            self.assertEqual(res_dict.get('code'), '0x1')

    # Container is not exist
    def test_stop_failed(self):
        req = dict(
            container_serial=self.ins.get('container_serial'),
            user_name=test_cfg.USER_NAME
        )
        with mock.patch.object(UiQueue, 'send'
                               ) as mock_queue_send:
            worker_res = dict(
                code='0x1',
                message='pass',
                container_serial=self.ins.get('container_serial')
            )
            mock_queue_send.return_value = json.dumps(worker_res)
            response = self.app.post('/stop_ins', data=json.dumps(req), follow_redirects=True)
            res_dict = json.loads(response.data)
            self.assertEqual(res_dict.get('code'), '0x9')

    def test_restart_success(self):
        create_instance(self.ins)
        req = dict(
            container_serial=self.ins.get('container_serial'),
            user_name=test_cfg.USER_NAME
        )
        with mock.patch.object(UiQueue, 'send'
                               ) as mock_queue_send:
            worker_res = dict(
                code='0x1',
                message='pass',
                container_serial=self.ins.get('container_serial')
            )
            mock_queue_send.return_value = json.dumps(worker_res)
            response = self.app.post('/restart_ins', data=json.dumps(req), follow_redirects=True)
            remove_instance_by_serial(self.ins.get('container_serial'))
            mock_queue_send.assert_called_once()
            res_dict = json.loads(response.data)
            self.assertEqual(res_dict.get('code'), '0x1')

    # Container is not exist
    def test_restart_failed(self):
        req = dict(
            container_serial=self.ins.get('container_serial'),
            user_name=test_cfg.USER_NAME
        )
        with mock.patch.object(UiQueue, 'send'
                               ) as mock_queue_send:
            worker_res = dict(
                code='0x1',
                message='pass',
                container_serial=self.ins.get('container_serial')
            )
            mock_queue_send.return_value = json.dumps(worker_res)
            response = self.app.post('/restart_ins', data=json.dumps(req), follow_redirects=True)
            res_dict = json.loads(response.data)
            self.assertEqual(res_dict.get('code'), '0x9')

    def test_remove_success(self):
        create_instance(self.ins)
        req = dict(
            container_serial=self.ins.get('container_serial'),
            user_name=test_cfg.USER_NAME
        )
        with mock.patch.object(UiQueue, 'send'
                               ) as mock_queue_send:
            worker_res = dict(
                code='0x1',
                message='pass',
                container_serial=self.ins.get('container_serial')
            )
            mock_queue_send.return_value = json.dumps(worker_res)
            response = self.app.post('/remove_ins', data=json.dumps(req), follow_redirects=True)
            remove_instance_by_serial(self.ins.get('container_serial'))
            mock_queue_send.assert_called_once()
            res_dict = json.loads(response.data)
            self.assertEqual(res_dict.get('code'), '0x1')

    def test_remove_failed(self):
        req = dict(
            container_serial=self.ins.get('container_serial'),
            user_name=test_cfg.USER_NAME
        )
        with mock.patch.object(UiQueue, 'send'
                               ) as mock_queue_send:
            worker_res = dict(
                code='0x1',
                message='pass',
                container_serial=self.ins.get('container_serial')
            )
            mock_queue_send.return_value = json.dumps(worker_res)
            response = self.app.post('/remove_ins', data=json.dumps(req), follow_redirects=True)
            res_dict = json.loads(response.data)
            self.assertEqual(res_dict.get('code'), '0x9')

if __name__ == '__main__':
    unittest.main()
