# -*-coding:Utf-8 -*-

"""Configuration file"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import os, sys, configparser

# Reading configuration from /etc if possible else form the script directory
conf = configparser.ConfigParser()
if os.path.isfile("/etc/passhport/passhport.ini"):
    conf.read("/etc/passhport/passhport.ini")
else:
    conf.read(sys.path[0] + "/passhport.ini")


""" Server configuration """
HOST =  conf.get("Network", "HOST")
PORT =  conf.get("Network", "PORT")

""" SSL Configuration """
SSL            = conf.getboolean("SSL", "SSL")
SSL_CERTIFICAT = conf.get("SSL", "SSL_CERTIFICAT")
SSL_KEY        = conf.get("SSL", "SSL_KEY")

url_passhport = "http" + SSL*"s" + "://" + HOST + ":" + PORT +"/"
certificate_path = conf.get("SSL", "SSL_CERTIFICAT")
