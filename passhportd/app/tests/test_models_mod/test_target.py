# -*-coding:Utf-8 -*-
import os

from nose.tools import *
from sqlalchemy import exc

from app import app, db
from app.models_mod import user, target
from config import basedir


class TestTarget:
    """Test for the class Target"""
    @classmethod
    def setup_class(cls):
        """Initialize configuration and create an empty database before
        testing
        """
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
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
        db.session.query(target.Target).delete()
        db.session.commit()

    def test_create(self):
        """Target creation in database succeeds"""
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = "54"
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"
        output      = """Targetname: clever_server\nHostname: 127.0.0.1\nPort: 54\nSSH options: --zap\nServertype: Bodhi\nAutocommand: ls -lh\nComment: Magnificent target\nUser list:\nUsergroup list:"""

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)
        db.session.add(t)
        db.session.commit()

        t_db = db.session.query(
            target.Target).filter_by(
            targetname="clever_server").first()

        assert_equal(t_db.targetname, targetname)
        assert_equal(t_db.hostname, hostname)
        assert_equal(str(t_db.port), port)
        assert_equal(t_db.sshoptions, sshoptions)
        assert_equal(t_db.servertype, servertype)
        assert_equal(t_db.autocommand, autocommand)
        assert_equal(t_db.comment, comment)
        assert_equal(repr(t_db), output)
