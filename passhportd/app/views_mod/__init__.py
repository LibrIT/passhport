# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import flask
from app import app

from .. import utilities as utils

@app.errorhandler(404)
def page_not_found(error):
    return utils.response("ERROR: You must fill the requested fields", 404)
