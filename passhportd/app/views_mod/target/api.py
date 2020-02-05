# -*-coding:Utf-8 -*-

from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import user, target, usergroup, exttargetaccess
from datetime import datetime, timedelta
import os

from .. import utilities as utils


@app.route("/api/target/list")
@app.route("/api/target/list/<name>")
def api_target_list(name=None):
    """Return a json formatted targets list from database"""
    result = []
    if not name:
        query = db.session.query(
                target.Target).order_by(
                target.Target.name).all()
    else:
        q = user.User.query.filter_by(name=name).first()
        query = [target for target in q.accessible_target_list() if target.targettype != "ssh"]

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


def listexttargetaccess(username):
    """List current open access for current user"""
    now = datetime.now()

    query  = db.session.query(exttargetaccess.Exttargetaccess) \
             .filter(exttargetaccess.Exttargetaccess.stopdate > str(now)).all()

    result = [taccess for taccess in query 
            if taccess.show_username() == username and taccess.proxy_pid != 0 ]
        
    return result


@app.route("/api/target/openedaccess/<name>")
def api_opened_access(name):
    """Return a json formatted target and connection infos for this user"""
    openaccess = listexttargetaccess(name)
    output = '{}'
    doneelt = []
    if openaccess:
        output = '{\n'
        for elt in openaccess:
            if not elt.show_targetname() in doneelt:
                doneelt.append(elt.show_targetname())
                output = output + '"' + elt.show_targetname() + '" : {\n'
                output = output + '"proxy_ip" : "' + elt.proxy_ip  + '",\n'
                output = output + '"proxy_port" : "' + str(elt.proxy_port) + '",\n'
                enddate = format(datetime.strptime(
                         elt.stopdate, "%Y-%m-%d %H:%M:%S.%f"), '%H:%M')
                output = output + '"enddate" : "' + enddate + '"},\n'
        output = output[:-2] + '\n}\n'

    return utils.response(output, 200)


@app.route("/api/accesstarget/list/<name>")
def api_target_specific_list(name):
    """Return a json formatted targets list from database for specific user"""
    result = []
    q = user.User.query.filter_by(name=name).first()
    accessibletargets = q.accessible_target_list()
    i = 0

    result.append("[")
    for entry in accessibletargets:
        if i == 0:
            i = 1
        else:
            result.append(",\n")
        result.append(entry.simplejson()[:-2] + ',\n"Lastconnection": "#TODO"\n}')
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
