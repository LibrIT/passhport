# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import app
from .views_mod import user, target, usergroup, targetgroup


@app.route("/")
def imalive():
    return """passhportd is running, gratz!"""
