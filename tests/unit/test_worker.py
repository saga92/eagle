#!/usr/bin/env python
#! -*- coding: utf-8 -*-

import unittest
import mock
import docker
import json
from base import UnitTest
from worker import worker
from tests import test_cfg
from dao import *


class TestWorker(UnitTest):

    def setUp(self):
        super(TestWorker, self).setUp()
        self.cli = worker.connect_docker_cli()
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

    def test_create_container_success(self):
        create_user(dict(
            username=test_cfg.USER_NAME,
            password=test_cfg.USER_PASSWORD,
            email=test_cfg.USER_EMAIL
        ))
        req = dict(
            image_id=test_cfg.CONTAINER_IMAGE_ID,
            user_name=test_cfg.USER_NAME,
            container_name=test_cfg.CONTAINER_NAME
        )
        with mock.patch.object(self.cli, 'create_container') as mock_cli_create:
            mock_cli_create.return_value = {'Id': test_cfg.CONTAINER_SERIAL}
            response = worker.create_container(self.cli, **req)
            remove_user_by_username(test_cfg.USER_NAME)
            remove_instance_by_serial(test_cfg.CONTAINER_SERIAL)
            mock_cli_create.assert_called_once()
            res_dict = json.loads(response)
            self.assertEqual(res_dict.get('code'), '0x1')

    # Exception: docker.errors.APIError
    def test_create_container_failed(self):
        create_user(dict(
            username=test_cfg.USER_NAME,
            password=test_cfg.USER_PASSWORD,
            email=test_cfg.USER_EMAIL
        ))
        req = dict(
            image_id=test_cfg.CONTAINER_IMAGE_ID,
            user_name=test_cfg.USER_NAME,
            container_name=test_cfg.CONTAINER_NAME
        )
        with mock.patch.object(self.cli, 'create_container') as mock_cli_create:
            mock_cli_create.side_effect = docker.errors.APIError(mock.Mock(), mock.Mock())
            response = worker.create_container(self.cli, **req)

            #The default container_serial is ''
            remove_instance_by_serial('')
            remove_user_by_username(test_cfg.USER_NAME)
            mock_cli_create.assert_called_once()
            res_dict = json.loads(response)
            self.assertEqual(res_dict.get('code'), '0x3')

    def test_run_container_success(self):
        create_instance(self.ins)
        req = dict(
            container_serial=test_cfg.CONTAINER_SERIAL,
            image_id=test_cfg.CONTAINER_IMAGE_ID,
            container_name=test_cfg.CONTAINER_NAME,
            user_name=test_cfg.USER_NAME
        )
        with mock.patch.object(self.cli, 'start'
                               ) as mock_cli_start,\
            mock.patch.object(self.cli, 'inspect_container'
                              ) as mock_cli_inspect:
            mock_cli_start.return_value = None
            mock_cli_inspect.return_value = {
                "NetworkSettings":{
                    "IPAddress": self.ins.get('host')
                }
            }
            response = worker.run_container(self.cli, **req)
            mock_cli_start.assert_called_once()
            remove_instance_by_serial(test_cfg.CONTAINER_SERIAL)
            mock_cli_inspect.assert_called_once()
            res_dict = json.loads(response)
            self.assertEqual(res_dict.get('code'), '0x1')

    # Exception: return value is not None
    def test_run_container_failed(self):
        create_instance(self.ins)
        req = dict(
            container_serial=test_cfg.CONTAINER_SERIAL,
            image_id=test_cfg.CONTAINER_IMAGE_ID,
            container_name=test_cfg.CONTAINER_NAME,
            user_name=test_cfg.USER_NAME
        )
        with mock.patch.object(self.cli, 'start') as mock_cli_start:

            #Return a value which is not None
            mock_cli_start.return_value = self.get_random_string()
            response = worker.run_container(self.cli, **req)
            remove_instance_by_serial(test_cfg.CONTAINER_SERIAL)
            mock_cli_start.assert_called_once()
            res_dict = json.loads(response)
            self.assertEqual(res_dict.get('code'), '0x2')

    def test_stop_container_success(self):
        create_instance(self.ins)
        req = dict(
            container_serial=test_cfg.CONTAINER_SERIAL,
            container_name=test_cfg.CONTAINER_NAME
        )
        with mock.patch.object(self.cli, 'stop') as mock_cli_stop:
            mock_cli_stop.return_value = None
            response = worker.stop_container(self.cli, **req)
            remove_instance_by_serial(test_cfg.CONTAINER_SERIAL)
            mock_cli_stop.assert_called_once()
            res_dict = json.loads(response)
            self.assertEqual(res_dict.get('code'), '0x1')

    def test_stop_container_failed(self):
        create_instance(self.ins)
        req = dict(
            container_serial=test_cfg.CONTAINER_SERIAL,
            container_name=test_cfg.CONTAINER_NAME
        )
        with mock.patch.object(self.cli, 'stop') as mock_cli_stop:
            mock_cli_stop.side_effect = docker.errors.NotFound(mock.Mock(), mock.Mock())
            response = worker.stop_container(self.cli, **req)
            remove_instance_by_serial(test_cfg.CONTAINER_SERIAL)
            mock_cli_stop.assert_called_once()
            res_dict = json.loads(response)
            self.assertEqual(res_dict.get('code'), '0x2')

    def test_restart_container_success(self):
        create_instance(self.ins)
        req = dict(
            container_serial=test_cfg.CONTAINER_SERIAL,
            container_name=test_cfg.CONTAINER_NAME
        )
        with mock.patch.object(self.cli, 'restart'
                               ) as mock_cli_restart,\
            mock.patch.object(self.cli, 'inspect_container'
                              ) as mock_cli_inspect:
            mock_cli_restart.return_value = None
            mock_cli_inspect.return_value = {
                "NetworkSettings":{
                    "IPAddress": self.ins.get('host')
                }
            }
            response = worker.restart_container(self.cli, **req)
            remove_instance_by_serial(test_cfg.CONTAINER_SERIAL)
            mock_cli_restart.assert_called_once()
            mock_cli_inspect.assert_called_once()
            res_dict = json.loads(response)
            self.assertEqual(res_dict['code'],'0x1')

    # Exception: docker.errors.NotFound
    def test_restart_container_failed(self):
        create_instance(self.ins)
        req = dict(
            container_serial=test_cfg.CONTAINER_SERIAL,
            container_name=test_cfg.CONTAINER_NAME
        )
        with mock.patch.object(self.cli, 'restart') as mock_cli_restart:
            mock_cli_restart.side_effect = docker.errors.NotFound(mock.Mock(), mock.Mock())
            response = worker.restart_container(self.cli, **req)
            remove_instance_by_serial(test_cfg.CONTAINER_SERIAL)
            mock_cli_restart.assert_called_once()
            res_dict = json.loads(response)
            self.assertEqual(res_dict['code'],'0x2')

    def test_remove_container_success(self):
        create_instance(self.ins)
        req = dict(
            container_serial=test_cfg.CONTAINER_SERIAL,
            container_name=test_cfg.CONTAINER_NAME
        )
        with mock.patch.object(self.cli, 'remove_container') as mock_cli_remove:
            mock_cli_remove.return_value = None
            response = worker.remove_container(self.cli, **req)
            mock_cli_remove.assert_called_once()
            res_dict = json.loads(response)
            self.assertEqual(res_dict['code'],'0x1')

    # Exception: docker.errors.NotFound
    def test_remove_container_failed(self):
        create_instance(self.ins)
        req = dict(
            container_serial=test_cfg.CONTAINER_SERIAL,
            container_name=test_cfg.CONTAINER_NAME
        )
        with mock.patch.object(self.cli, 'remove_container') as mock_cli_remove:
            mock_cli_remove.side_effect = docker.errors.NotFound(mock.Mock(), mock.Mock())
            response = worker.remove_container(self.cli, **req)
            remove_instance_by_serial(test_cfg.CONTAINER_SERIAL)
            mock_cli_remove.assert_called_once()
            res_dict = json.loads(response)
            self.assertEqual(res_dict['code'],'0x2')

if __name__ == '__main__':
    unittest.main()
