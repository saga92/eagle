#!/usr/bin/env python
# -*- coding: utf-8 -*-

DOCKER_CLI_URL = 'unix://var/run/docker.sock'

MAC = False

IMAGE_DICT = {1: 'eagle-ubuntu:14.04', 2: 'eagle-centos:7', 3: \
        'eagle-fedora:23', 4: 'eagle-debian:8'}

UI_HOST = 'http://127.0.0.1:8088'

CREATE = 1
STOP = 2
REMOVE = 3
RESTART = 4

RUNNING_INSTANCE = 1
STOP_INSTANCE = 2
FAILED_INSTANCE = 3
PENDING_INSTANCE = 4