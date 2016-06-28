#!/usr/bin/env python
# -*- coding: utf-8 -*-

DOCKER_CLI_URL = 'unix://var/run/docker.sock'

MAC = False

IMAGE_DICT = {1: 'eagle-ubuntu:14.04', 2: 'eagle-centos:7', 3: \
        'eagle-fedora:23', 4: 'eagle-debian:8'}

UI_HOST = 'http://127.0.0.1:8088'

CREATE_INSTANCE = 1

STOP_INSTANCE = 2

REMOVE_INSTANCE = 3

RESTART_INSTANCE = 4

FAILED_INSTANCE = 5

PENDING_INSTANCE = 6