# -*-coding:Utf-8 -*-

from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import user, target, usergroup
import os

from .. import utilities as utils


@app.route("/api/user/list")
def api_user_list():
    """Return a json formatted users list from database"""
    result = []
    query = db.session.query(
        user.User).order_by(
        user.User.name).all()
    i = 0

    result.append("[")
    for entry in query:
        if i == 0:
            i = 1
        else:
            result.append(",\n")
        result.append(entry.simplejson())
    result.append("]")


    if not result:
        return utils.response("No user in database.", 200)

    return utils.response("".join(result), 200)

@app.route("/api/user/show/<name>")
def api_user_show(name):
    """Return  json formated data about a user"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: User's name is required ", 417)

    user_data = user.User.query.filter_by(name=name).first()

    if user_data is None:
        return utils.response("ERROR: No user with the name " + name + \
                " in the database.", 417)

    return utils.response("[" + str(user_data.simplejson()) + "]", 200)

