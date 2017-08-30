# -*-coding:Utf-8 -*-

from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import user, target, targetgroup
import os

from .. import utilities as utils


@app.route("/api/targetgroup/list")
def api_targetgroup_list():
    """Return a json formatted targetgroup list from database"""
    result = []
    query = db.session.query(
        targetgroup.Targetgroup).order_by(
        targetgroup.Targetgroup.name).all()
    i = 0

    result.append("[")
    for entry in query:
        if i == 0:
            i = 1
        else:
            result.append(",\n")
        result.append( entry.simplejson())
    result.append("]")


    if not result:
        return "No targetgroup in database.", 200, \
            {"content-type": "text/plain; charset=utf-8"}

    return "".join(result), 200, \
        {"content-type": "text/plain; charset=utf-8"}
