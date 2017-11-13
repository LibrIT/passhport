# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import user, target, usergroup, targetgroup
from . import api

from .. import utilities as utils


@app.route("/targetgroup/list")
def targetgroup_list():
    """Return the targetgroup list of database"""
    result = []
    query = db.session.query(
        targetgroup.Targetgroup.name).order_by(
        targetgroup.Targetgroup.name)

    for row in query.all():
        result.append(str(row[0]))

    if not result:
        return "No targetgroup in database.", 200, \
            {"content-type": "text/plain; charset=utf-8"}

    return "\n".join(result), 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/targetgroup/search/<pattern>")
def targetgroup_search(pattern):
    """Return a list of targetgroups that match the given pattern"""
    result = []
    query = db.session.query(
        targetgroup.Targetgroup.name).filter(
        targetgroup.Targetgroup.name.like("%" + pattern + "%"))

    for row in query.all():
        result.append(str(row[0]))

    if not result:
        return 'No targetgroup matching the pattern "' + pattern + \
            '" found.', 200, {"content-type": "text/plain; charset=utf-8"}

    return "\n".join(result), 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/targetgroup/show/<name>")
def targetgroup_show(name):
    """Return all data about a targetgroup"""
    # Check for required fields
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    targetgroup_data = targetgroup.Targetgroup.query.filter_by(
        name=name).first()

    if targetgroup_data is None:
        return 'ERROR: No targetgroup with the name "' + name + \
            '" in the database.', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    return targetgroup_data.__repr__(), 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/targetgroup/create", methods=["POST"])
def targetgroup_create():
    """Add a targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    name = request.form["name"]
    comment = request.form["comment"]

    # Check for required fields
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check unicity for name
    query = db.session.query(targetgroup.Targetgroup.name)\
        .filter_by(name=name).first()

    if query is not None:
        return 'ERROR: The name "' + name + \
            '" is already used by another targetgroup ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    t = targetgroup.Targetgroup(
        name=name,
        comment=comment)
    db.session.add(t)

    # Try to add the targetgroup in the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + name + '" -> ' + \
            e.message, 409, {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + name + '" -> created', 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/targetgroup/edit", methods=["POST"])
def targetgroup_edit():
    """Edit a targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    name = request.form["name"]
    new_name = request.form["new_name"]
    new_comment = request.form["new_comment"]

    # Check required fields
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check if the name exists in the database
    query = db.session.query(targetgroup.Targetgroup.name).filter_by(
        name=name).first()

    if query is None:
        return 'ERROR: No targetgroup with the name "' + name + \
            '" in the database.', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    to_update = db.session.query(
        targetgroup.Targetgroup).filter_by(
        name=name)

    # Let's modify only relevent fields
    if new_comment:
        # This specific string allows admins to remove old comments
        if new_comment == "PASSHPORTREMOVECOMMENT":
            new_comment = ""
        to_update.update({"comment": new_comment})
    if new_name:
        # Check unicity for name
        query = db.session.query(targetgroup.Targetgroup.name)\
            .filter_by(name=new_name).first()

        if query is not None and new_name != query.name:
            return 'ERROR: The name "' + new_name + \
                '" is already used by another targetgroup ', \
                417, {"content-type": "text/plain; charset=utf-8"}

        to_update.update({"name": new_name})

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + name + '" -> ' + \
            e.message, 409, {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + name + '" -> edited', 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/targetgroup/delete/<name>")
def targetgroup_delete(name):
    """Delete a targetgroup in the database"""
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check if the name exists
    query = db.session.query(targetgroup.Targetgroup.name)\
        .filter_by(name=name).first()

    if query is None:
        return 'ERROR: No targetgroup with the name "' + name + \
            '" in the database.', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    db.session.query(
        targetgroup.Targetgroup).filter(
        targetgroup.Targetgroup.name == name).delete()

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + name + '" -> ' + \
            e.message, 409, {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + name + '" -> deleted', 200, \
        {"content-type": "text/plain; charset=utf-8"}

@app.route("/targetgroup/adduser", methods=["POST"])
def targetgroup_adduser():
    """Add a user in the targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    username = request.form["username"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not username or not targetgroupname:
        return "ERROR: The username and targetgroupname are required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Targetgroup and user have to exist in database
    u = utils.get_user(username)
    if not u:
        return 'ERROR: no user "' + username + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Now we can add the user
    tg.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + username + '" added to "' + targetgroupname + '"', 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/targetgroup/rmuser", methods=["POST"])
def targetgroup_rmuser():
    """Remove a user from the targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    username = request.form["username"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not username or not targetgroupname:
        return "ERROR: The username and targetgroupname are required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # User and targetgroup have to exist in database
    u = utils.get_user(username)
    if not u:
        return 'ERROR: no user "' + username + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check if the given user is a member of the given targetgroup
    if not tg.username_in_targetgroup(username):
        return 'ERROR: The user "' + username + \
            '" is not a member of the targetgroup "' + \
            targetgroupname + '" ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Now we can remove the user
    tg.rmuser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + username + '" removed from "' + \
        targetgroupname + '"', 200, \
        {"content-type": "text/plain; charset=utf-8"}

@app.route("/targetgroup/addtarget", methods=["POST"])
def targetgroup_addtarget():
    """Add a target in the targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    targetname = request.form["targetname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not targetname or not targetgroupname:
        return "ERROR: The targetname and targetgroupname are required ",
        417, {"content-type": "text/plain; charset=utf-8"}

    # Target and targetgroup have to exist in database
    t = utils.get_target(targetname)
    if not t:
        return 'ERROR: no target "' + targetname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Now we can add the target
    tg.addtarget(t)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + targetname + '" added to "' + \
        targetgroupname + '"', 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/targetgroup/rmtarget", methods=["POST"])
def targetgroup_rmtarget():
    """Remove a target from the targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    targetname = request.form["targetname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not targetname or not targetgroupname:
        return "ERROR: The targetname and targetgroupname are required ",
        417, {"content-type": "text/plain; charset=utf-8"}

    # Target and targetgroup have to exist in database
    t = utils.get_target(targetname)
    if not t:
        return 'ERROR: No target "' + targetname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: No targetgroup "' + targetgroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check if the given target is a member of the given targetgroup
    if not tg.targetname_in_targetgroup(targetname):
        return 'ERROR: The target "' + target + \
            '" is not a member of the targetgroup "' + \
            targetgroupname + '" ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Now we can remove the target
    tg.rmtarget(t)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + targetname + '" removed from "' + \
        targetgroupname + '"', 200, \
        {"content-type": "text/plain; charset=utf-8"}

@app.route("/targetgroup/addusergroup", methods=["POST"])
def targetgroup_addusergroup():
    """Add a usergroup in the targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not usergroupname or not targetgroupname:
        return "ERROR: The usergroupname and targetgroupname are required ",
        417, {"content-type": "text/plain; charset=utf-8"}

    # Usergroup and targetgroup have to exist in database
    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return 'ERROR: no usergroup "' + usergroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Now we can add the usergroup
    tg.addusergroup(ug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + usergroupname + '" added to "' + \
        targetgroupname + '"', 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/targetgroup/rmusergroup", methods=["POST"])
def targetgroup_rmusergroup():
    """Remove a usergroup from the targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not usergroupname or not targetgroupname:
        return "ERROR: The usergroupname and targetgroupname are required ",
        417, {"content-type": "text/plain; charset=utf-8"}

    # Usergroup and targetgroup have to exist in database
    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return 'ERROR: no usergroup "' + usergroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check if the given usergroup is a member of the given targetgroup
    if not tg.usergroupname_in_targetgroup(usergroupname):
        return 'ERROR: The usergroup "' + usergroupname + \
            '" is not a member of the targetgroup "' + \
            targetgroupname + '" ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Now we can remove the usergroup
    tg.rmusergroup(ug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + usergroupname + '" removed from "' + \
        targetgroupname + '"', 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/targetgroup/addtargetgroup", methods=["POST"])
def targetgroup_addtargetgroup():
    """Add a targetgroup (subtargetgroup) in the targetgroup
    in the database
    """
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    subtargetgroupname = request.form["subtargetgroupname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not subtargetgroupname or not targetgroupname:
        return "ERROR: The subtargetgroupname and targetgroupname "
        "are required ", 417, {"content-type": "text/plain; charset=utf-8"}

    # Subtargetgroup and targetgroup have to exist in database
    stg = utils.get_targetgroup(subtargetgroupname)
    if not stg:
        return 'ERROR: no targetgroup "' + subtargetgroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Now we can add the subtargetgroup
    if not tg.addtargetgroup(stg):
        if tg == stg:
            return "ERROR: impossible to add a targetgroup into itself.", \
                    417, {"content-type": "text/plain; charset=utf-8"}

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + subtargetgroupname + '" added to "' + \
        targetgroupname + '"', 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/targetgroup/rmtargetgroup", methods=["POST"])
def targetgroup_rmtargetgroup():
    """Remove a targetgroup (subtargetgroup) from the targetgroup
    in the database
    """
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    subtargetgroupname = request.form["subtargetgroupname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not subtargetgroupname or not targetgroupname:
        return "ERROR: The subtargetgroupname and targetgroupname "
        "are required ", 417, {"content-type": "text/plain; charset=utf-8"}

    # Subtargetgroup and targetgroup have to exist in database
    stg = utils.get_targetgroup(subtargetgroupname)
    if not stg:
        return 'ERROR: no targetgroup "' + subtargetgroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check if the given subtargetgroup is a member of the given targetgroup
    if not tg.subtargetgroupname_in_targetgroup(subtargetgroupname):
        return 'ERROR: The subtargetgroup "' + subtargetgroupname + \
            '" is not a member of the targetgroup "' + \
            targetgroupname + '" ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Now we can remove the subtargetgroup
    tg.rmtargetgroup(stg)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + subtargetgroupname + '" removed from "' + \
        targetgroupname + '"', 200, \
        {"content-type": "text/plain; charset=utf-8"}
