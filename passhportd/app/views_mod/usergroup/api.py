# -*-coding:Utf-8 -*-

from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import user, target, usergroup
import os

from .. import utilities as utils


@app.route("/api/usergroup/list")
def api_usergroup_list():
    """Return a json formatted usergroup list from database"""
    result = []
    query = db.session.query(
        usergroup.Usergroup).order_by(
        usergroup.Usergroup.name).all()
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
        return utils.response("No usergroup in database.", 200)

    return utils.response("\n".join(result), 200)
