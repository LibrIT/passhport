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
        result.append(entry.simplejson())
    result.append("]")


    if not result:
        return utils.response("No target in database.", 200)

    return utils.response("".join(result), 200)


@app.route("/api/target/show/<name>")
def api_target_show(name):
    """Return  json formated data about a target"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: Target's name is required ", 417)

    target_data = target.Target.query.filter_by(name=name).first()

    if target_data is None:
        return utils.response("ERROR: No target with the name " + name + \
                " in the database.", 417)

    return utils.response("[" + str(target_data.simplejson()) + "]", 200)


@app.route("/api/target/user/<name>")
def api_target_user(name):
    """Return json formated list of users attached to the target"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    target_data = target.Target.query.filter_by(name=name).first()

    if target_data is None:
        return utils.response('ERROR: No target with the name "' + name + \
                '" in the database.', 417)

    return api_target_element(target_data, "user") 


@app.route("/api/target/usergroup/<name>")
def api_target_usergroup(name):
    """Return json formated list of usergroups attached to the target"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    target_data = target.Target.query.filter_by(name=name).first()

    if target_data is None:
        return utils.response('ERROR: No target with the name "' + name + \
                '" in the database.', 417)

    return api_target_element(target_data, "usergroup") 
    

def api_target_element(target_data, element):
    """Return the attached elements to a target"""
    if element == "user":
        return utils.response("[" + target_data.username_list_json() + \
                              "]", 200)
    elif element == "usergroup":
        return utils.response("[" + target_data.usergroupname_list_json() + \
                              "]", 200)
