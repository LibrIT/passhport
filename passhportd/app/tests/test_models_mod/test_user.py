# -*-coding:Utf-8 -*-
import os

from nose.tools import *
from sqlalchemy import exc

from app import app, db
from app.models_mod import user
from config import basedir


class TestUser:
    """Test for the class User"""
    @classmethod
    def setup_class(cls):
        """Initialize configuration and create an empty database before
        testing
        """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
            os.path.join(basedir, "test.db")
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
        email = "john@example.com"
        sshkey  = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com"""
        comment = "This is a great comment"
        output  = """Email: john@example.com\nSSH key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com\nComment: This is a great comment"""

        u = user.User(
            email=email.encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))
        db.session.add(u)
        db.session.commit()

        u_db = db.session.query(
            user.User).filter_by(
            email="john@example.com").first()

        assert_equal(u_db.email, email)
        assert_equal(u_db.sshkey, sshkey)
        assert_equal(u_db.comment, comment)
        assert_equal(repr(u_db), output)

    @raises(exc.IntegrityError)
    def test_create_existing_email(self):
        """User creation in database with an already used email fails
        """
        email = "john@example.com"
        sshkey  = """ssh-rsa AAAAB3NzEaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john2@example.com"""
        comment = "A random comment man"

        u = user.User(
            email=email.encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))
        db.session.add(u)
        db.session.commit()

        u = user.User(
            email=email.encode("utf8"),
            sshkey="""Another sshkey""".encode("utf8"),
            comment=comment.encode("utf8"))
        db.session.add(u)
        db.session.commit()

    @raises(exc.IntegrityError)
    def test_create_existing_sshkey(self):
        """User creation in database with an already used sshkey fails
        """
        email = "john@example.com"
        sshkey  = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com"""
        comment = "An awesome comment man"

        u = user.User(
            email=email.encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))
        db.session.add(u)
        db.session.commit()

        u = user.User(
            email="smith@example.com".encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))
        db.session.add(u)
        db.session.commit()

    # We should test if an empty email while creating a user raises an error, but it seems that SQLite doesn't check it
    # def test_create_empty_email(self):

    # We should test if an empty sshkey while creating a user raises an error, but it seems that SQLite doesn't check it
    # def test_create_empty_sshkey(self):

    def test_edit(self):
        """User edition in database succeeds"""
        email = "example@test.org"
        sshkey      = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT example@test.org"""
        comment = "That comment"
        new_email = "oh@yeah.net"
        new_sshkey  = """A short key"""
        new_comment = "A new comment"

        u = user.User(
            email=email.encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))

        db.session.add(u)
        db.session.commit()

        user_to_edit = db.session.query(
            user.User).filter_by(
            email="example@test.org".encode("utf8"))
        updated_rows = user_to_edit.update(
            {
                "email": new_email.encode("utf8"),
                "sshkey": new_sshkey.encode("utf8"),
                "comment": new_comment.encode("utf8")})
        db.session.commit()

        u_edit = db.session.query(
            user.User).filter_by(
            email=new_email.encode("utf8")).first()

        assert_equal(updated_rows, 1)
        assert_equal(u.id, u_edit.id)
        assert_equal(u_edit.email, new_email)
        assert_equal(u_edit.sshkey, new_sshkey)
        assert_equal(u_edit.comment, new_comment)

    def test_edit_non_existing_user(self):
        """User edition of a non existing user in database does nothing
        (but doesn't raise error)
        """
        u = db.session.query(
            user.User).filter_by(
            email="random@alea.info".encode("utf8"))
        updated_rows = u.update({"email": "bat@man.com".encode(
            "utf8"), "sshkey": "batmobile".encode("utf8"), "comment": "So d4rk".encode("utf8")})

        assert_equal(updated_rows, 0)

        db.session.commit()

    @raises(exc.IntegrityError)
    def test_edit_existing_email(self):
        """User edition with a new email already used in database fails
        """
        email = "rocket@man.net"
        sshkey = "railway"
        comment = "speedy"
        email2 = "john@caffe.net"
        sshkey2 = "coffeshop"
        comment2 = "slow"

        u = user.User(
            email=email.encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))
        u2 = user.User(
            email=email2.encode("utf8"),
            sshkey=sshkey2.encode("utf8"),
            comment=comment2.encode("utf8"))

        db.session.add(u)
        db.session.commit()
        db.session.add(u2)
        db.session.commit()

        u2 = db.session.query(user.User).filter_by(email=email2.encode("utf8"))
        updated_rows = u2.update({"email": email.encode("utf8")})

        db.session.commit()

    @raises(exc.IntegrityError)
    def test_edit_existing_sshkey(self):
        """User edition with a new sshkey already used in database
        fails
        """
        email = "rocket@man.net"
        sshkey = "railway"
        comment = "speedy"
        email2 = "john@caffe.net"
        sshkey2 = "coffeshop"
        comment2 = "slow"

        u = user.User(
            email=email.encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))
        u2 = user.User(
            email=email2.encode("utf8"),
            sshkey=sshkey2.encode("utf8"),
            comment=comment2.encode("utf8"))

        db.session.add(u)
        db.session.commit()
        db.session.add(u2)
        db.session.commit()

        u2 = db.session.query(user.User).filter_by(email=email2.encode("utf8"))
        updated_rows = u2.update({"sshkey": sshkey.encode("utf8")})

        db.session.commit()

    def test_show(self):
        """User show in database succeeds"""
        email = "viridian@red.color"
        sshkey = "redkey"
        comment = "unusual comment"

        u = user.User(
            email=email.encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))
        db.session.add(u)
        db.session.commit()

        user_data = user.User.query.filter_by(
            email=email.encode("utf8")).first()

        assert_equal(email, user_data.email)
        assert_equal(sshkey, user_data.sshkey)
        assert_equal(comment, user_data.comment)

    def test_show_non_existing_user(self):
        """User show a non existing user in database does nothing
        (but doesn't raise error)
        """
        user_data = user.User.query.filter_by(
            email="the@mail.net".encode("utf8")).first()

        assert_is_none(user_data)

    def test_delete(self):
        """User deletion in database succeeds"""
        email = "john@example.com"
        sshkey  = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com"""
        comment = "This is a great comment"

        u = user.User(
            email=email.encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))
        db.session.add(u)
        db.session.commit()

        db.session.delete(u)
        db.session.commit()

        u_db = db.session.query(
            user.User).filter_by(
            email="john@example.com".encode("utf8")).first()

        assert_is_none(u_db)

    @raises(exc.InvalidRequestError)
    def test_delete_non_existing_user(self):
        """User deletion with a non existing user fails"""
        email = "dude@bait.org"
        sshkey  = """A great keyblade"""
        comment = "Nice comment"

        u = user.User(
            email=email.encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))
        db.session.delete(u)
        db.session.commit()

    def test_list_no_users(self):
        """User listing with no user in database succeeds"""
        query = db.session.query(
            user.User.email).order_by(
            user.User.email).all()

        assert_equal(query, [])

    def test_list_existing_users(self):
        """User listing with existing users in database succeeds"""
        email = "john@example.com"
        sshkey    = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDAdH3Dwen9fNgBxZ+QrR3wt9TSQt1+kizp9uz6heudbZ9J6+xghvDnTmwhcm7MROLXG9FMHPtDXNviVmwa/Pj/EQp/2390XT8BLy9/yYpfMrbYSSJEcnchd7EA1U1txjc5mQbWTxiXFcM6UifwF1cjJrOda0OZpR+BdoEkpLrkyuTOWgdV5zoVu0pLrSJNdHAFEtPZ0yaTuX3ufk3ScSeIdXyj4qaX/T0mIuXmfP89yy0ipFMiimXvi/D2Q+MMDAjbDQuW1YlX730hgKJTZD+X5RkNHFHpggTLpvvRDffhqxuBvQNNgUk0hPQ6gFgQIgVIgjIiJkM/j0Ayig+k+4hT john@example.com"""
        comment = "This is a great comment"
        user_list = []

        u = user.User(
            email=email.encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))
        db.session.add(u)
        db.session.commit()

        query = db.session.query(
            user.User.email).order_by(
            user.User.email).all()
        for row in query:
            user_list.append(str(row[0]))

        user_list = "".join(user_list)

        assert_equal(user_list, "john@example.com")

    def test_search(self):
        """User search with users matching pattern in database succeeds
        """
        email = "rocket@man.net"
        sshkey = "railway"
        comment = "speedy"
        email2 = "john@caffe.org"
        sshkey2 = "coffeshop"
        comment2 = "slow"
        res_list = []

        u = user.User(
            email=email.encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))
        u2 = user.User(
            email=email2.encode("utf8"),
            sshkey=sshkey2.encode("utf8"),
            comment=comment2.encode("utf8"))
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()

        query = db.session.query(
            user.User.email).filter(
            user.User.email.like(
                '%' +
                ".net" +
                '%')).all()

        for row in query:
            res_list.append(str(row[0]))

        res_list = "\n".join(res_list)

        assert_equal(res_list, "rocket@man.net")

    def test_search_empty_pattern(self):
        """User searching with an empty pattern returns all users
        in database succeeds
        """
        email = "rocket@man.net"
        sshkey = "railway"
        comment = "speedy"
        email2 = "john@caffe.org"
        sshkey2 = "coffeshop"
        comment2 = "slow"
        res_list = []

        u = user.User(
            email=email.encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))
        u2 = user.User(
            email=email2.encode("utf8"),
            sshkey=sshkey2.encode("utf8"),
            comment=comment2.encode("utf8"))

        db.session.add(u)
        db.session.add(u2)
        db.session.commit()

        query = db.session.query(
            user.User.email).filter(
            user.User.email.like(
                '%' +
                "" +
                '%')).all()

        for row in query:
            res_list.append(str(row[0]))

        res_list = "\n".join(res_list)

        assert_equal(res_list, "john@caffe.org\nrocket@man.net")

    def test_search_no_users_match_pattern(self):
        """User searching with a pattern that no user match with
        in database returns nothing succeeds
        """
        email = "rocket@man.net"
        sshkey = "railway"
        comment = "speedy"
        res_list = []

        u = user.User(
            email=email.encode("utf8"),
            sshkey=sshkey.encode("utf8"),
            comment=comment.encode("utf8"))

        db.session.add(u)
        db.session.commit()

        query = db.session.query(
            user.User.email).filter(
            user.User.email.like(
                '%' +
                "zu" +
                '%')).all()

        for row in query:
            res_list.append(str(row[0]))

        res_list = "\n".join(res_list)

        assert_equal(res_list, "")
