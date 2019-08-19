# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import os

from nose.tools import *
from sqlalchemy import exc

from app import app, db
from app.models_mod import user
#from config import basedir


class TestUser:
    """Test for the class User"""
    @classmethod
    def setup_class(cls):
        """Initialize configuration and create an empty database before
        testing
        """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        cls.app = app.test_client()
        db.create_all()

    @classmethod
    def teardown_class(cls):
        """Delete the database created for testing"""
        db.session.remove()
        db.drop_all()

    def setUp(self):
        """Does nothing"""
        pass

    def tearDown(self):
        """Rollback after raising a database exception for testing"""
        db.session.rollback()
        db.session.query(user.User).delete()
        db.session.commit()

    def test_create(self):
        """User creation in database succeeds"""
        name = "john@example.com"
        sshkey  = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com"""
        comment = "This is a great comment"
        output  = """Email: john@example.com\nSSH key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com\nComment: This is a great comment\nAccessible target list: \n\nDetails in access:\nAccessible directly: \nAccessible through usergroups: \nAccessible through targetgroups: """

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)
        db.session.add(u)
        db.session.commit()

        u_db = db.session.query(
            user.User).filter_by(
            name="john@example.com").first()

        assert_equal(u_db.name, name)
        assert_equal(u_db.sshkey, sshkey)
        assert_equal(u_db.comment, comment)
       
        assert_equal(repr(u_db), output)

    @raises(exc.IntegrityError)
    def test_create_existing_name(self):
        """User creation in database with an already used name fails
        """
        name = "john@example.com"
        sshkey  = """ssh-rsa AAAAB3NzEaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john2@example.com"""
        comment = "A random comment man"

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)
        db.session.add(u)
        db.session.commit()

        u = user.User(
            name=name,
            sshkey="""Another sshkey""",
            comment=comment)
        db.session.add(u)
        db.session.commit()

    @raises(exc.IntegrityError)
    def test_create_existing_sshkey(self):
        """User creation in database with an already used sshkey fails
        """
        name = "john@example.com"
        sshkey  = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com"""
        comment = "An awesome comment man"

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)
        db.session.add(u)
        db.session.commit()

        u = user.User(
            name="smith@example.com",
            sshkey=sshkey,
            comment=comment)
        db.session.add(u)
        db.session.commit()

    # We should test if an empty name while creating a user raises
    # an error, but it seems that SQLite doesn't check it
    # def test_create_empty_name(self):

    # We should test if an empty sshkey while creating a user raises
    # an error, but it seems that SQLite doesn't check it
    # def test_create_empty_sshkey(self):

    def test_edit(self):
        """User edition in database succeeds"""
        name = "example@test.org"
        sshkey      = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT example@test.org"""
        comment = "That comment"
        new_name = "oh@yeah.net"
        new_sshkey  = """A short key"""
        new_comment = "A new comment"

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)

        db.session.add(u)
        db.session.commit()

        user_to_edit = db.session.query(
            user.User).filter_by(
            name="example@test.org")
        updated_rows = user_to_edit.update(
            {
                "name": new_name,
                "sshkey": new_sshkey,
                "comment": new_comment})
        db.session.commit()

        u_edit = db.session.query(
            user.User).filter_by(
            name=new_name).first()

        assert_equal(updated_rows, 1)
        assert_equal(u.id, u_edit.id)
        assert_equal(u_edit.name, new_name)
        assert_equal(u_edit.sshkey, new_sshkey)
        assert_equal(u_edit.comment, new_comment)

    def test_edit_non_existing_user(self):
        """User edition of a non existing user in database does nothing
        (but doesn't raise error)
        """
        u = db.session.query(
            user.User).filter_by(
            name="random@alea.info")
        updated_rows = u.update({"name": "bat@man.com",
            "sshkey": "batmobile", "comment": "So d4rk"})

        assert_equal(updated_rows, 0)

        db.session.commit()

    @raises(exc.IntegrityError)
    def test_edit_existing_name(self):
        """User edition with a new name already used in database fails
        """
        name = "rocket@man.net"
        sshkey = "railway"
        comment = "speedy"
        name2 = "john@caffe.net"
        sshkey2 = "coffeshop"
        comment2 = "slow"

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)
        u2 = user.User(
            name=name2,
            sshkey=sshkey2,
            comment=comment2)

        db.session.add(u)
        db.session.commit()
        db.session.add(u2)
        db.session.commit()

        u2 = db.session.query(user.User).filter_by(name=name2)
        updated_rows = u2.update({"name": name})

        db.session.commit()

    @raises(exc.IntegrityError)
    def test_edit_existing_sshkey(self):
        """User edition with a new sshkey already used in database
        fails
        """
        name = "rocket@man.net"
        sshkey = "railway"
        comment = "speedy"
        name2 = "john@caffe.net"
        sshkey2 = "coffeshop"
        comment2 = "slow"

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)
        u2 = user.User(
            name=name2,
            sshkey=sshkey2,
            comment=comment2)

        db.session.add(u)
        db.session.commit()
        db.session.add(u2)
        db.session.commit()

        u2 = db.session.query(user.User).filter_by(name=name2)
        updated_rows = u2.update({"sshkey": sshkey})

        db.session.commit()

    def test_show(self):
        """User show in database succeeds"""
        name = "viridian@red.color"
        sshkey = "redkey"
        comment = "unusual comment"

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)
        db.session.add(u)
        db.session.commit()

        user_data = user.User.query.filter_by(
            name=name).first()

        assert_equal(name, user_data.name)
        assert_equal(sshkey, user_data.sshkey)
        assert_equal(comment, user_data.comment)

    def test_show_non_existing_user(self):
        """User show a non existing user in database does nothing
        (but doesn't raise error)
        """
        user_data = user.User.query.filter_by(
            name="the@mail.net").first()

        assert_is_none(user_data)

    def test_delete(self):
        """User deletion in database succeeds"""
        name = "john@example.com"
        sshkey  = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com"""
        comment = "This is a great comment"

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)
        db.session.add(u)
        db.session.commit()

        db.session.delete(u)
        db.session.commit()

        u_db = db.session.query(
            user.User).filter_by(
            name="john@example.com").first()

        assert_is_none(u_db)

    @raises(exc.InvalidRequestError)
    def test_delete_non_existing_user(self):
        """User deletion with a non existing user fails"""
        name = "dude@bait.org"
        sshkey  = """A great keyblade"""
        comment = "Nice comment"

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)
        db.session.delete(u)
        db.session.commit()

    def test_list_no_users(self):
        """User listing with no user in database succeeds"""
        query = db.session.query(
            user.User.name).order_by(
            user.User.name).all()

        assert_equal(query, [])

    def test_list_existing_users(self):
        """User listing with existing users in database succeeds"""
        name = "john@example.com"
        sshkey    = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com"""
        comment = "This is a great comment"
        user_list = []

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)
        db.session.add(u)
        db.session.commit()

        query = db.session.query(
            user.User.name).order_by(
            user.User.name).all()
        for row in query:
            user_list.append(str(row[0]))

        user_list = "".join(user_list)

        assert_equal(user_list, "john@example.com")

    def test_search(self):
        """User search with users matching pattern in database succeeds
        """
        name = "rocket@man.net"
        sshkey = "railway"
        comment = "speedy"
        name2 = "john@caffe.org"
        sshkey2 = "coffeshop"
        comment2 = "slow"
        res_list = []

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)
        u2 = user.User(
            name=name2,
            sshkey=sshkey2,
            comment=comment2)
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()

        query = db.session.query(
            user.User.name).filter(
            user.User.name.like(
                '%' +
                ".net" +
                '%')).order_by(
                    user.User.name).all()

        for row in query:
            res_list.append(str(row[0]))

        res_list = "\n".join(res_list)

        assert_equal(res_list, "rocket@man.net")

    def test_search_empty_pattern(self):
        """User searching with an empty pattern returns all users
        in database succeeds
        """
        name = "rocket@man.net"
        sshkey = "railway"
        comment = "speedy"
        name2 = "john@caffe.org"
        sshkey2 = "coffeshop"
        comment2 = "slow"
        res_list = []

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)
        u2 = user.User(
            name=name2,
            sshkey=sshkey2,
            comment=comment2)

        db.session.add(u)
        db.session.add(u2)
        db.session.commit()

        query = db.session.query(
            user.User.name).filter(
            user.User.name.like(
                '%' +
                "" +
                '%')).order_by(
                    user.User.name).all()

        for row in query:
            res_list.append(str(row[0]))

        res_list = "\n".join(res_list)

        assert_equal(res_list, "john@caffe.org\nrocket@man.net")

    def test_search_no_users_match_pattern(self):
        """User searching with a pattern that no user match with
        in database returns nothing succeeds
        """
        name = "rocket@man.net"
        sshkey = "railway"
        comment = "speedy"
        res_list = []

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)

        db.session.add(u)
        db.session.commit()

        query = db.session.query(
            user.User.name).filter(
            user.User.name.like(
                '%' +
                "zu" +
                '%')).order_by(
                    user.User.name).all()

        for row in query:
            res_list.append(str(row[0]))

        res_list = "\n".join(res_list)

        assert_equal(res_list, "")
