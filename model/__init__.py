#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from user import User
from instance import Image, Instance
