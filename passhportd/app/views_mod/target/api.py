# -*-coding:Utf-8 -*-

from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import user, target, usergroup
import os

from .. import utilities as utils


@app.route("/api/target/list")
def api_target_list():
    """Return a json formatted targets list from database"""
    result = []
    query = db.session.query(
        target.Target).order_by(
        target.Target.name).all()
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
        return "No target in database.", 200, \
            {"content-type": "text/plain; charset=utf-8"}

    return "".join(result), 200, \
        {"content-type": "text/plain; charset=utf-8"}
