# -*- coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals
from io import open

import os, sys, stat
import config

from ldap3 import Server, Connection, ALL
from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import user, target, logentry
from .. import utilities as utils



@app.route("/logentry/list")
def logentry_list():
    """Return the logentries list of database"""
    result = []
    query = db.session.query(logentry.Logentry).all()

    for row in query:
        result.append(row)

    if not result:
        return utils.response("No Log entry in database.", 200)

    return utils.response("\n".join(result), 200)


def linklog(logentry, user, target):
    """Link the logentry to a target and a user"""
    u = utils.get_user(user)
    u.addlogentry(logentry)
    t = utils.get_target(target)
    t.addlogentry(logentry)


@app.route("/logentry/create", methods=["POST"])
def logentry_create():
    """Add a logentry in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    l = logentry.Logentry(
        connectiondate = request.form["connectiondate"],
        connectioncmd  = request.form["connectioncmd"],
        logfilepath   = request.form["logfilepath"],
        logfilename   = request.form["logfilename"])
    db.session.add(l)
    
    #Link this logentry with the user and the target
    linklog(l, request.form["user"], request.form["target"])

    # Try to add the Logentry on the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + e.message , 409)

    return utils.response('OK: Log entry -> created', 200)

