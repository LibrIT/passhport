#!/usr/bin/env python
import os
import unittest

from config import basedir
from app import app, db
from app.models_mod import user

class TestUser(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_creation(self):
        username    = 'john'
        email       = 'john@example.com'
        sshkey      = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com'
        comment     = 'This is a great comment'
        output      = """Username: john\nEmail: john@example.com\nSshkey: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com\nComment: This is a great comment\n"""

        u = user.User(username=username, email=email, sshkey=sshkey, comment=comment)

        # Assertions
        assert u.username[0:len(username)]  == username
        assert u.email[0:len(email)]        == email
        assert u.sshkey[0:len(sshkey)]      == sshkey
        assert u.comment[0:len(comment)]    == comment
        assert str(u) == str(output)

#TODO   Test if a user with an already existing name is rejected.
#       Test if a user with sshkey or login empty is rejected


if __name__ == '__main__':
        unittest.main()
