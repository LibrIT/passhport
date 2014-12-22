#!/usr/bin/env python
import os
import unittest

from config import basedir
from app import app, db
from app.models_mod import user, target

class TestTarget(unittest.TestCase):
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
        targetname  = 'myserver'
        hostname    = '127.0.0.1'
        port        = ''
        sshoptions  = '-z'
        servertype  = 'Debian'
        autocommand = 'ls -l'
        comment     = 'This is a great target'
        output      = 'Targetname: myserver\nHostname: 127.0.0.1\nPort: None\nSshoptions: -z\nServertype: Debian\nAutocommand: ls -l\nComment: This is a great target\n'


        t = target.Target(targetname=targetname, hostname=hostname, sshoptions=sshoptions, servertype=servertype, autocommand=autocommand, comment=comment)

        # Assertions
        assert t.targetname[0:len(targetname)]  == targetname
        assert t.hostname[0:len(hostname)]     == hostname
        assert t.sshoptions[0:len(sshoptions)]  == sshoptions
        assert t.servertype[0:len(servertype)]  == servertype
        assert t.autocommand[0:len(autocommand)]== autocommand
        assert t.comment[0:len(comment)]        == comment
        assert str(t) == str(output)

#TODO   Test if an already existing name is rejected.
#       Test all the mandatory fields


if __name__ == '__main__':
        unittest.main()
