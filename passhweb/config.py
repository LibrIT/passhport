# -*-coding:Utf-8 -*-

"""Configuration file reader"""
import os
import sys
import configparser

# Reading configuration from /etc if possible else form the script directory
conf = configparser.ConfigParser()
conffile = "passhweb.ini"
if os.path.isfile("/etc/passhport/" + conffile):
    conf.read("/etc/passhport/" + conffile)
else:
    conf.read(sys.path[0] + "/" + conffile)


""" Server configuration """
HOSTNAME =  conf.get("Network", "LISTENING_IP")
PORT =  conf.get("Network", "PORT")
PASSHPORTD_HOSTNAME =  conf.get("Network", 'PASSHPORTD_HOSTNAME')
PASSHPORTD_PORT =  conf.get("Network", "PASSHPORTD_PORT")

""" SSL Configuration """
SSL            = conf.getboolean("SSL", "SSL")
SSL_CERTIFICAT = conf.get("SSL", "SSL_CERTIFICAT")

url_passhportd = "http" + SSL*"s" + "://" + \
                               PASSHPORTD_HOSTNAME + ":" + PASSHPORTD_PORT +"/"
certificate_path = conf.get("SSL", "SSL_CERTIFICAT")

""" Misc """
DEBUG = conf.getboolean("Misc", "DEBUG", fallback=False)
# Allow a username to connect without the right password when LDAP enabled
LOGINNOPWD  = conf.get("Misc", "LOGINNOPWD", fallback=False)
FIRSTLAUNCH = conf.get("Misc", "FIRSTLAUNCH",
            fallback=os.path.exists("/home/passhport/passhport/passhweb/.neverlaunched"))
SECRET = conf.get("Misc", "SECRET")

""" Module configuration """
# To enable LDAP you must configure passhportd
LDAP           = conf.getboolean("Modules", "LDAP", fallback=False)
# Databases protection module is reserved for enterprise version
DBP            = conf.get("Modules", "DBP", 
                            fallback=os.path.exists("/home/passhport/passhdb"))

""" Configuration paths """
PUBSSH = conf.get("ConfigFiles", "PUBSSH",
            fallback="/home/passhport/passhweb/passhconfig/sshkey.pub")
PRIVSSH = conf.get("ConfigFiles", "PRIVSSH",
            fallback="/home/passhport/passhweb/passhconfig/sshkey")
SSLCERT = conf.get("ConfigFiles", "SSLCERT",
            fallback="/home/passhport/passhweb/passhconfig/ssl.cert")
SSLKEY  = conf.get("ConfigFiles", "SSLKEY",
            fallback="/home/passhport/passhweb/passhconfig/ssl.key")

