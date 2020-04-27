# -*-coding:Utf-8 -*-

"""Configuration file reader"""
import os, sys, configparser

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
DEBUG = conf.getboolean("Misc", "DEBUG")

""" SSL Configuration """
SSL            = conf.getboolean("SSL", "SSL")
SSL_CERTIFICAT = conf.get("SSL", "SSL_CERTIFICAT")

url_passhportd = "http" + SSL*"s" + "://" + PASSHPORTD_HOSTNAME + ":" + PASSHPORTD_PORT +"/"
certificate_path = conf.get("SSL", "SSL_CERTIFICAT")
