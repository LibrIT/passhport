# -*-coding:Utf-8 -*-
import os

from nose.tools import *
from sqlalchemy import exc

from app            import app, db
from app.models_mod import user
from config         import basedir

class TestUser:
    """Test for the class User"""
    @classmethod
    def setup_class(cls):
        """Initialize configuration and create an empty database before testing"""
        app.config['TESTING']                 = True
        app.config['WTF_CSRF_ENABLED']        = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "test.db")
        cls.app                               = app.test_client()
        db.create_all()

    @classmethod
    def teardown_class(cls):
        """Delete the database created for testing"""
        db.session.remove()
        db.drop_all()

    def test_create(self):
        """User creation function succeeds"""
        email   = "john@example.com"
        sshkey  = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com"""
        comment = "This is a great comment"
        output  = """Email: john@example.com\nSSH key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com\nComment: This is a great comment"""

        u = user.User(email = email, sshkey = sshkey, comment = comment)
        db.session.add(u)

        db.session.commit()

        assert_equal(u.email, email)
        assert_equal(u.sshkey, sshkey)
        assert_equal(u.comment, comment)
        assert_equal(repr(u), output)

    @raises(exc.IntegrityError)
    def test_create_existing_email(self):
        """User creation function with an already used email fails"""
        email   = "john@example.com"
        sshkey  = """ssh-rsa AAAAB3NzEaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john2@example.com"""
        comment = "A random comment man"

        u = user.User(email = email, sshkey = sshkey, comment = comment)
        db.session.add(u)

        db.session.commit()
