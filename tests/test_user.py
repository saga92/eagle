#!/usr/bin/env python
# -*- cooding: utf-8 -*-

import unittest
import json
from view import *
from base import Test


class TestUser(Test):

    def test_signup_success(self):
        pass

    def test_signup_email_repeat(self):
        pass

    def test_signup_name_repeat(self):
        pass

    def test_signin_success(self):
        pass

    def test_signin_name_error(self):
        pass

    def test_sigin_email_error(self):
        pass

    def test_sigin_password_error(self):
        pass

    def test_session(self):
        pass

    def test_signout(self):
        pass

if __name__ == '__main__':
    unittest.main()