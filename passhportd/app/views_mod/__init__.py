# -*-coding:Utf-8 -*-

import flask
from app import app

from . import utilities as utils

@app.errorhandler(404)
def page_not_found(error):
    return utils.response("ERROR: You must fill the requested fields", 404)
