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


@app.route("/api/usergroup/show/<name>")
def api_usergroup_show(name):
    """Return  json formated data about a usergroup"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: Usergroup's name is required ", 417)

    usergroup_data = usergroup.Usergroup.query.filter_by(name=name).first()

    if usergroup_data is None:
        return utils.response("ERROR: No usergroup with the name " + name + \
                " in the database.", 417)

    return utils.response("[" + str(usergroup_data.simplejson()) + "]", 200)


@app.route("/api/usergroup/<element>/<name>")
def api_usergroup_element(name, element):
    """Return json formated users lists attached to the usergroup 'name'"""
    usergroup_data = usergroup.Usergroup.query.filter_by(name=name).first()

    if usergroup_data is None:
        return utils.response("ERROR: No usergroup with the name " + name + \
                " in the database.", 417)

    return api_usergroup_element(usergroup_data, element)

    
def api_usergroup_element(usergroup_data, element):
    """Return the attached elements to a usergroup"""
    if element == "user":
        return utils.response("[" + usergroup_data.username_list_json() + \
                              "]", 200)
    elif element == "manager" :
        return utils.response("[" + usergroup_data.managername_list_json() + \
                              "]", 200)
    elif element == "usergroup":
        return utils.response("[" + usergroup_data.usergroupname_list_json() + \
                              "]", 200)
