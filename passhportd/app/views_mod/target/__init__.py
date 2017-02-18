# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import user, target, usergroup

from .. import utilities as utils


@app.route("/target/list")
def target_list():
    """Return the target list of database"""
    result = []
    query = db.session.query(
        target.Target.name).order_by(
        target.Target.name).all()

    for row in query:
        result.append(row[0])

    if not result:
        return "No target in database.", 200, \
            {"content-type": "text/plain; charset=utf-8"}

    return "\n".join(result), 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/target/search/<pattern>")
def target_search(pattern):
    """Return a list of targets that match the given pattern"""
    result = []
    query  = db.session.query(target.Target.name)\
        .filter(target.Target.name.like("%" + pattern + "%"))\
        .order_by(target.Target.name).all()

    for row in query:
        result.append(row[0])

    if not result:
        return 'No target matching the pattern "' + pattern + \
            '" found.', 200, {"content-type": "text/plain; charset=utf-8"}

    return "\n".join(result), 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/target/show/<name>")
def target_show(name):
    """Return all data about a target"""
    # Check for required fields
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    target_data = target.Target.query.filter_by(name=name).first()

    if target_data is None:
        return 'ERROR: No target with the name "' + name + \
            '" in the database.', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    return str(target_data), 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/target/port/<name>")
def target_port(name):
    """Return port related to a target"""
    # Check for required fields
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    target_data = target.Target.query.filter_by(name=name).first()

    if target_data is None:
        return 'ERROR: No target with the name "' + name + \
            '" in the database.', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    port = target_data.port

    # If there is no port declared, we assume it's 22
    if port is None:
        print("No port set on " + name + ", 22 is used")
        port = "22"
    else:
        port = str(port).replace(" ","")
    
    return port, 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/target/login/<name>")
def target_login(name):
    """Return login related to a target"""
    # Check for required fields
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    target_data = target.Target.query.filter_by(name=name).first()

    if target_data is None:
        return 'ERROR: No target with the name "' + name + \
            '" in the database.', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    login = target_data.login

    # If there is no user declared, we assume it's root
    if login is None:
        print("No login set on " + name + ", root is used")
        login = "root"
    else:
        login = str(login).replace(" ","")
    
    return login, 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/target/sshoptions/<name>")
def target_options(name):
    """Return options related to a target"""
    # Check for required fields
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    target_data = target.Target.query.filter_by(name=name).first()

    if target_data is None:
        return 'ERROR: No target with the name "' + name + \
            '" in the database.', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    return str(target_data.sshoptions), 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/target/create", methods=["POST"])
def target_create():
    """Add a target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    name = request.form["name"]
    hostname = request.form["hostname"]
    login = request.form["login"]
    port = request.form["port"]
    sshoptions = request.form["sshoptions"]
    comment = request.form["comment"]

    # Check for required fields
    if not name or not hostname:
        return "ERROR: The name and hostname are required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    if not login:
        login = "root"

    if not port:
        port = 22

    # Check unicity for name
    query = db.session.query(target.Target.name)\
        .filter_by(name=name).first()

    if query is not None:
        return 'ERROR: The name "' + name + \
            '" is already used by another target ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    t = target.Target(
        name=name,
        hostname=hostname,
        login=login,
        port=port,
        sshoptions=sshoptions,
        comment=comment)
    db.session.add(t)

    # Try to add the target on the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + name + '" -> ' + e.message, 409, \
                {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + name + '" -> created', 200, \
            {"content-type": "text/plain; charset=utf-8"}


@app.route("/target/edit", methods=["POST"])
def target_edit():
    """Edit a target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    name = request.form["name"]
    new_name = request.form["new_name"]
    new_hostname = request.form["new_hostname"]
    new_login = request.form["new_login"]
    new_port = request.form["new_port"]
    new_sshoptions = request.form["new_sshoptions"]
    new_comment = request.form["new_comment"]

    # Check required fields
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check if the name exists in the database
    query = db.session.query(target.Target.name)\
        .filter_by(name=name).first()

    if query is None:
        return 'ERROR: No target with the name "' + name + \
            '" in the database.', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    to_update = db.session.query(target.Target.name).filter_by(name=name)

    # Let's modify only relevent fields
    if new_login:
        to_update.update({"login": new_login})

    if new_sshoptions:
        to_update.update({"sshoptions": new_sshoptions})

    if new_comment:
        # This specific string allows admins to remove old comments
        if new_comment == "PASSHPORTREMOVECOMMENT":
            new_comment = ""
        to_update.update({"comment": new_comment})

    if new_port:
        to_update.update({"port": new_port})

    if new_hostname:
        to_update.update({"hostname": new_hostname})

    if new_name:
        # Check unicity for name
        query = db.session.query(target.Target.name)\
            .filter_by(name=new_name).first()

        if query is not None and new_name != query.name:
            return 'ERROR: The name "' + new_name + \
                '" is already used by another target ', \
                417, {"content-type": "text/plain; charset=utf-8"}

        to_update.update({"name": new_name})

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + name + '" -> ' + e.message, 409, {
            "Content-Type": "text/plain"}

    return 'OK: "' + name + '" -> edited', 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/target/delete/<name>")
def target_delete(name):
    """Delete a target in the database"""
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check if the name exists
    query = db.session.query(target.Target.name)\
        .filter_by(name=name).first()

    if query is None:
        return 'ERROR: No target with the name "' + name + \
            '" in the database.', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    db.session.query(
        target.Target).filter(
        target.Target.name == name).delete()

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + name + '" -> ' + e.message, 409, \
            {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + name + '" -> deleted', 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/target/adduser", methods=["POST"])
def target_adduser():
    """Add a user in the target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    username = request.form["username"]
    targetname = request.form["targetname"]

    # Check for required fields
    if not username or not targetname:
        return "ERROR: The username and targetname are required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # User and target have to exist in database
    u = utils.get_user(username)
    if not u:
        return 'ERROR: no user "' + username + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    t = utils.get_target(targetname)
    if not t:
        return 'ERROR: no target "' + targetname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Now we can add the user
    t.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetname + '" -> ' + e.message, 409, \
            {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + username + '" added to "' + targetname + '"', 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/target/rmuser", methods=["POST"])
def target_rmuser():
    """Remove a user from the target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    username = request.form["username"]
    targetname = request.form["targetname"]

    # Check for required fields
    if not username or not targetname:
        return "ERROR: The username and targetname are required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # User and target have to exist in database
    u = utils.get_user(username)
    if not u:
        return 'ERROR: No user "' + username + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    t = utils.get_target(targetname)
    if not t:
        return 'ERROR: No target "' + targetname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check if the given user is a member of the given target
    if not t.username_in_target(username):
        return 'ERROR: The user "' + username + \
            '" is not a member of the target "' + \
            targetname + '" ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Now we can remove the user
    t.rmuser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetname + '" -> ' + e.message, 409, \
            {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + username + '" removed from "' + \
        targetname + '"', 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/target/addusergroup", methods=["POST"])
def target_addusergroup():
    """Add a usergroup in the target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    targetname = request.form["targetname"]

    # Check for required fields
    if not usergroupname or not targetname:
        return "ERROR: The usergroupname and targetname are required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Usergroup and target have to exist in database
    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return 'ERROR: no usergroup "' + usergroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    t = utils.get_target(targetname)
    if not t:
        return 'ERROR: no target "' + targetname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Now we can add the user
    t.addusergroup(ug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetname + '" -> ' + e.message, 409, \
            {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + usergroupname + '" added to "' + \
        targetname + '"', 200, {"content-type": "text/plain; charset=utf-8"}


@app.route("/target/rmusergroup", methods=["POST"])
def target_rmusergroup():
    """Remove a usergroup from the target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    targetname = request.form["targetname"]

    # Check for required fields
    if not usergroupname or not targetname:
        return "ERROR: The usergroupname and targetname are required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Usergroup and target have to exist in database
    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return 'ERROR: No usergroup "' + usergroupname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    t = utils.get_target(targetname)
    if not t:
        return 'ERROR: No target "' + targetname + \
            '" in the database ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check if the given usergroup is a member of the given target
    if not t.usergroupname_in_target(usergroupname):
        return 'ERROR: The usergroup "' + usergroupname + \
            '" is not a member of the target "' + \
            targetname + '" ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Now we can remove the usergroup
    t.rmusergroup(ug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetname + '" -> ' + e.message, 409, \
            {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + usergroupname + '" removed from "' + \
        targetname + '"', 200, {"content-type": "text/plain; charset=utf-8"}
