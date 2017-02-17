# -*-coding:Utf-8 -*-

"""Configuration file"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import os

""" Server configuration """
HOST = 'localhost'
PORT = '5000'

""" SSL Configuration """
SSL            = True
SSL_CERTIFICAT = os.environ["HOME"] + "/certs/cert.pem"
SSL_KEY        = os.environ["HOME"] + "/certs/key.pem"


