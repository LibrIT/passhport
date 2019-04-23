# -*-coding:Utf-8 -*-
import os

from nose.tools import *
import unittest

from app import app, db
from app.views_mod import user


TEST_DB = '/tmp/test.db'

class UserTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
	

    def tearDown(self):
        pass


    def test_root(self):
        """ Test default answer"""
        rv = self.app.get('/', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'passhportd is running, gratz!\n', rv.data)


