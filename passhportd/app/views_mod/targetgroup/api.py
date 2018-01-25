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
        return utils.response("No targetgroup in database.", 200)

    return utils.response("".join(result), 200)


@app.route("/api/targetgroup/show/<name>")
def api_targetgroup_show(name):
    """Return  json formated data about a targetgroup"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: Targetgroup's name is required ", 417)

    targetgroup_data = targetgroup.Targetgroup.query.filter_by(name=name).first()

    if targetgroup_data is None:
        return utils.response("ERROR: No targetgroup with the name " + name + \
                " in the database.", 417)

    return utils.response("[" + str(targetgroup_data.simplejson()) + "]", 200)


@app.route("/api/targetgroup/<element>/<name>")
def api_targetgroup_element(name, element):
    """Return json formated element lists attached to the targetgroup 'name'"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    targetgroup_data = targetgroup.Targetgroup.query.filter_by(name=name).first()

    if targetgroup_data is None:
        return utils.response("ERROR: No targetgroup with the name " + name + \
                " in the database.", 417)

    return api_targetgroup_element(targetgroup_data, element)


def api_targetgroup_element(targetgroup_data, element):
    """Return the attached elements to a targetgroup"""
    if element == "user":
        return utils.response("[" + targetgroup_data.username_list_json() + \
                              "]", 200)
    elif element == "usergroup":
        return utils.response("[" + \
                   targetgroup_data.usergroupname_list_json() + "]", 200)
    elif element == "target":
        return utils.response("[" + targetgroup_data.targetname_list_json() + \
                              "]", 200)
    elif element == "targetgroup":
        return utils.response("[" + \
                   targetgroup_data.targetgroupname_list_json() + "]", 200)
    else: 
        return utils.response("Error: element type unkown" , 417)

