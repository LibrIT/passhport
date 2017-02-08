# -*-coding:Utf-8 -*-

"""Configuration file"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import os

"""Database (SQLite by default)"""
basedir = os.path.expanduser("~")
datadir = os.path.join(basedir, "var")

SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_DIR = datadir
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(datadir, "app.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(datadir, "db_repository")

""" SSH Keyfile """
SSH_KEY_FILE = os.environ["HOME"] + "/.ssh/authorized_keys"

""" PaSSHport path """
PASSHPORT_PATH= os.environ["HOME"] + "/passhport/passhport/passhport"
PYTHON_PATH= os.environ["HOME"] + "/passhport-run-env/bin/python3"

""" Server configuration """
HOST = '127.0.0.1'


""" SSL Configuration """
SSL            = True
SSL_CERTIFICAT = os.environ["HOME"] + "/certs/cert.pem"
SSL_KEY        = os.environ["HOME"] + "/certs/key.pem"


