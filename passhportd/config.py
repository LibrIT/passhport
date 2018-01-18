# -*-coding:Utf-8 -*-

"""Configuration file reader"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import os, sys, configparser

# Reading configuration from /etc if possible else form the script directory
conf = configparser.ConfigParser()
conffile = "passhportd.ini"
if os.path.isfile("/etc/passhport/" + conffile):
    conf.read("/etc/passhport/" + conffile)
else:
    conf.read(sys.path[0] + "/" + conffile)

# Reading the configuration
"""Database (SQLite by default)"""
SQLALCHEMY_TRACK_MODIFICATIONS = conf.getboolean("Database", \
                                "SQLALCHEMY_TRACK_MODIFICATIONS")
SQLALCHEMY_DATABASE_DIR = conf.get("Database", \
                                "SQLALCHEMY_DATABASE_DIR")
SQLALCHEMY_DATABASE_URI = conf.get("Database", \
                                "SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_MIGRATE_REPO = conf.get("Database", \
                                "SQLALCHEMY_MIGRATE_REPO")
""" SSH Keyfile """
SSH_KEY_FILE = conf.get("Environment", "SSH_KEY_FILE")

""" PaSSHport path """
PASSHPORT_PATH = conf.get("Environment", "PASSHPORT_PATH")
PYTHON_PATH = conf.get("Environment", "PYTHON_PATH")

""" Server configuration """
HOST =  conf.get("Network", "LISTENING_IP")

""" LDAP configuration """
LDAPURI = conf.get("LDAP", "LDAP_PROVIDER_URL")
LDAPPORT = int(conf.get("LDAP", "LDAP_PORT"))
LDAPBASE = conf.get("LDAP", "LDAP_USER_BASEDN")
LDAPFIELD = conf.get("LDAP", "LDAP_LOGIN_SEARCH_FIELD")
LDAPACC = conf.get("LDAP", "LDAP_ACC")
LDAPPASS = conf.get("LDAP", "LDAP_PASS")

""" SSL Configuration """
SSL            = conf.get("SSL", "SSL")
SSL_CERTIFICAT = conf.get("SSL", "SSL_CERTIFICAT")
SSL_KEY        = conf.get("SSL", "SSL_KEY")



