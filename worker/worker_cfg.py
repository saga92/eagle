#!/usr/bin/env python
# -*- coding: utf-8 -*-

DOCKER_CLI_URL = 'unix://var/run/docker.sock'

MAC = False

IMAGE_DICT = {1: 'eagle-ubuntu:latest', 2: 'eagle-centos:latest', 3: \
        'eagle-fedora:latest', 4: 'eagle-debian:latest'}

UI_HOST = 'http://127.0.0.1:8088'

CREATE_INSTANCE = 1

STOP_INSTANCE = 2

REMOVE_INSTANCE = 3

RESTART_INSTANCE = 4
