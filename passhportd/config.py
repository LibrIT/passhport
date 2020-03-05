# -*-coding:Utf-8 -*-

"""Configuration file reader"""
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
SQLALCHEMY_TRACK_MODIFICATIONS  = conf.getboolean("Database", \
                                    "SQLALCHEMY_TRACK_MODIFICATIONS")
SQLALCHEMY_DATABASE_DIR         = conf.get("Database", \
                                    "SQLALCHEMY_DATABASE_DIR")
SQLALCHEMY_DATABASE_URI         = conf.get("Database", \
                                    "SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_MIGRATE_REPO         = conf.get("Database", \
                                    "SQLALCHEMY_MIGRATE_REPO")
""" SALT for password storage """
SALT            = conf.get("Database", "SALT")

""" SSH Keyfile """
SSH_KEY_FILE    = conf.get("Environment", "SSH_KEY_FILE")

""" PaSSHport path """
OPEN_ACCESS_PATH= conf.get("Environment", "OPEN_ACCESS_PATH")
PASSHPORT_PATH  = conf.get("Environment", "PASSHPORT_PATH")
PYTHON_PATH     = conf.get("Environment", "PYTHON_PATH")

""" Server configuration """
HOST            =  conf.get("Network", "LISTENING_IP")

""" LDAP configuration """
LDAPURI         = conf.get("LDAP", "LDAP_PROVIDER_URL", fallback='undefined')
LDAPPORT        = conf.getint("LDAP", "LDAP_PORT", fallback='389')
LDAPBASE        = conf.get("LDAP", "LDAP_USER_BASEDN", fallback='undefined')
LDAPFIELD       = conf.get("LDAP", "LDAP_LOGIN_SEARCH_FIELD", fallback='undefined')
LDAPACC         = conf.get("LDAP", "LDAP_ACC", fallback='undefined')
LDAPPASS        = conf.get("LDAP", "LDAP_PASS", fallback='undefined')

""" SSL Configuration """
SSL             = conf.get("SSL", "SSL")
SSL_CERTIFICAT  = conf.get("SSL", "SSL_CERTIFICAT")
SSL_KEY         = conf.get("SSL", "SSL_KEY")


""" NOTIFICATIONS """
NOTIF_LOG_TYPE  = conf.get("NOTIFICATIONS", "NOTIF_LOG_TYPE", fallback='None')
NOTIF_TO        = conf.get("NOTIFICATIONS", "NOTIF_TO", fallback='root')
NOTIF_FROM      = conf.get("NOTIFICATIONS", "NOTIF_FROM", fallback='passhport@bastion')
NOTIF_SMTP      = conf.get("NOTIFICATIONS", "SMTP", fallback='127.0.0.1')

""" MISC """
MAXLOGSIZE      = conf.get("MISC", "MAXLOGSIZE")
NODE_NAME       = conf.get("MISC", "NODE_NAME")
DB_SESSIONS_TO  = conf.get("MISC", "DB_SESSIONS_TO", fallback='4')
