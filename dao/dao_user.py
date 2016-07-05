# Copyright (c) the Eagle authors and contributors.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime
from utils import db
from model import User

def update_col_by_id(id, *args, **kwargs):
    db_session = db.Session()
    user_query_res = db_session.query(User).filter(User.id == id).first()
    for key in kwargs:
        setattr(user_query_res, key, kwargs.get(key))
    db_session.commit()

def update_password_by_id(id, password):
    update_user(id, password=password)

def update_email_by_id(id, email):
    update_user(id, email=email)

def update_salt_by_id(id, salt):
    update_user(id, salt=salt)

def update_create_time_by_id(id, create_time):
    update_user(id, create_time=create_time)

def update_update_time_by_id(id, update_time):
    update_user(id, update_time=update_time)

def update_is_deleted_by_id(id, is_deleted):
    update_user(id, is_deleted=is_deleted)

def create_user(user):
    db_session = db.Session()
    password = hashlib.md5(user.get('password') + user.get('salt', '')).hexdigest()
    user_res = User(user.get('username'), password,
                    email=user.get('email'), salt=user.get('salt', ''),
                    create_time=user.get('create_time', datetime.utcnow()),
                    update_time=user.get('update_time', datetime.utcnow()),
                    is_deleted=user.get('is_deleted', 0)
                    )
    db_session.add(user_res)
    db_session.commit()

def get_user_by_username(username):
    db_session = db.Session()
    user_query_res = db_session.query(User).filter(User.username == username).first()
    return user_query_res

def remove_user_by_username(username):
    db_session = db.Session()
    user_query_res = db_session.query(User).filter(User.username == username).first()
    user_name = user_query_res.username
    db_session.delete(user_query_res)
    db_session.commit()
    return user_name
