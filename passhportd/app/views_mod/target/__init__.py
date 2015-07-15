# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import app
from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import target, user, usergroup


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
        return "No target in database.", 200, {"Content-Type": "text/plain"}

    return "\n".join(result), 200, {"Content-Type": "text/plain"}


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
            '" found.', 200, {"Content-Type": "text/plain"}

    return "\n".join(result), 200, {"Content-Type": "text/plain"}


@app.route("/target/show/<name>")
def target_show(name):
    """Return all data about a user"""
    # Check for required fields
    if not name:
        return "ERROR: The name is required ", 417, {
            "Content-Type": "text/plain"}

    target_data = target.Target.query.filter_by(name=name).first()

    if target_data is None:
        return 'ERROR: No target with the name "' + name + \
            '" in the database.', 417, {"Content-Type": "text/plain"}

    return str(target_data), 200, {"Content-Type": "text/plain"}


@app.route("/target/create", methods=["POST"])
def target_create():
    """Add a target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    name = request.form["name"]
    hostname = request.form["hostname"]
    port = request.form["port"]
    sshoptions = request.form["sshoptions"]
    servertype = request.form["servertype"]
    autocommand = request.form["autocommand"]
    comment = request.form["comment"]

    # Check for required fields
    if not name or not hostname:
        return "ERROR: The name and hostname are required ", 417, {
            "Content-Type": "text/plain"}

    if not port:
        port = 22

    # Check unicity for name
    query = db.session.query(target.Target.name)\
        .filter_by(name=name).first()

    if query is not None:
        return 'ERROR: The name "' + name + \
            '" is already used by another target ',\
             417, {"Content-Type": "text/plain"}

    t = target.Target(
        name=name,
        hostname=hostname,
        port=port,
        sshoptions=sshoptions,
        servertype=servertype,
        autocommand=autocommand,
        comment=comment)
    db.session.add(t)

    # Try to add the target on the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + name + '" -> ' + e.message, 409, \
                {"Content-Type": "text/plain"}

    return 'OK: "' + name + '" -> created', 200, \
            {"Content-Type": "text/plain"}


@app.route("/target/edit", methods=["POST"])
def target_edit():
    """Edit a target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    name = request.form["name"]
    new_name = request.form["new_name"]
    new_hostname = request.form["new_hostname"]
    new_port = request.form["new_port"]
    new_sshoptions = request.form["new_sshoptions"]
    new_servertype = request.form["new_servertype"]
    new_autocommand = request.form["new_autocommand"]
    new_comment = request.form["new_comment"]

    # Check required fields
    if not name:
        return "ERROR: The name is required ", 417, {
            "Content-Type": "text/plain"}

    # Check if the name exists in the database
    query = db.session.query(target.Target)\
        .filter_by(name=name).first()

    if query is None:
        return 'ERROR: No target with the name "' + name + \
            '" in the database.', 417, {"Content-Type": "text/plain"}

    toupdate = db.session.query(target.Target).filter_by(name=name)

    # Let's modify only relevent fields
    if new_sshoptions:
        toupdate.update({"sshoptions": new_sshoptions})
    if new_servertype:
        toupdate.update({"servertype": new_servertype})
    if new_autocommand:
        toupdate.update({"autocommand": new_autocommand})
    if new_comment:
        toupdate.update({"comment": new_comment})
    if new_port:
        toupdate.update({"port": new_port})
    if new_hostname:
        toupdate.update({"hostname": new_hostname})
    if new_name:
        # Check unicity for name
        query = db.session.query(target.Target.name)\
            .filter_by(name=new_name).first()

        if query is not None and new_name != query.name:
            return 'ERROR: The name "' + new_name + \
                '" is already used by another target ', \
                417, {"Content-Type": "text/plain"}

        toupdate.update({"name": new_name})

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + name + '" -> ' + e.message, 409, {
            "Content-Type": "text/plain"}

    return 'OK: "' + name + '" -> edited', 200, {
        "Content-Type": "text/plain"}


@app.route("/target/delete/<name>")
def target_delete(name):
    """Delete a target in the database"""
    if not name:
        return "ERROR: The name is required ", 417, {
            "Content-Type": "text/plain"}

    # Check if the name exists
    query = db.session.query(target.Target.name)\
        .filter_by(name=name).first()

    if query is None:
        return 'ERROR: No target with the name "' + name + \
            '" in the database.', 417, {"Content-Type": "text/plain"}

    db.session.query(
        target.Target).filter(
        target.Target.name == name).delete()

    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return 'ERROR: "' + name + '" -> ' + e.message, 409, {
            "Content-Type": "text/plain"}

    return 'OK: "' + name + '" -> deleted', 200, {
        "Content-Type": "text/plain"}


@app.route("/target/adduser", methods=["POST"])
def target_adduser():
    """Add a user in the target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetname = request.form["targetname"]
    username = request.form["username"]

    # Check for mandatory fields
    if not targetname or not username:
        return "ERROR: The targetname and username are required ", 417, {
            "Content-Type": "text/plain"}

    # Target and user have to exist in database
    t = get_target(targetname)
    if not t:
        return 'ERROR: no target "' + targetname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    u = get_user(username)
    if not u:
        return 'ERROR: no user "' + username + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Now we can add the user
    t.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetname + '" -> ' + e.message, 409, {
            "Content-Type": "text/plain"}

    return 'OK: "' + username + '" added to "' + targetname + \
        '"', 200, {"Content-Type": "text/plain"}


@app.route("/target/rmuser", methods=["POST"])
def target_rmuser():
    """Remove a user from the target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetname = request.form["targetname"]
    username = request.form["username"]

    # Check for mandatory fields
    if not targetname or not username:
        return "ERROR: The targetname and name are required ", 417, {
            "Content-Type": "text/plain"}

    # Target and user have to exist in database
    t = get_target(targetname)
    if not t:
        return 'ERROR: No target "' + targetname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    u = get_user(username)
    if not u:
        return 'ERROR: No user "' + username + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Check if the given user is a member of the given target
    if not t.name_in_target(username):
        return 'ERROR: The user "' + username + \
            '" is not a member of the target "' + \
            targetname + '" ', 417, {"Content-Type": "text/plain"}

    # Now we can remove the user
    t.rmuser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetname + '" -> ' + e.message, 409, {
            "Content-Type": "text/plain"}

    return 'OK: "' + username + '" removed from "' + \
        targetname + '"', 200, {"Content-Type": "text/plain"}


@app.route("/target/addusergroup", methods=["POST"])
def target_addusergroup():
    """Add a usergroup in the target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetname = request.form["targetname"]
    usergroupname = request.form["usergroupname"]

    # Check for mandatory fields
    if not targetname or not usergroupname:
        return "ERROR: The targetname and usergroupname are required ", 417, {
            "Content-Type": "text/plain"}

    # Target and user have to exist in database
    t = get_target(targetname)
    if not t:
        return 'ERROR: no target "' + targetname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    g = get_usergroup(usergroupname)
    if not g:
        return 'ERROR: no usergroup "' + usergroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Now we can add the user
    t.addusergroup(g)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetname + '" -> ' + e.message, 409, {
            "Content-Type": "text/plain"}

    return 'OK: "' + usergroupname + '" added to "' + \
        targetname + '"', 200, {"Content-Type": "text/plain"}


@app.route("/target/rmusergroup", methods=["POST"])
def target_rmusergroup():
    """Remove a usergroup from the target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetname = request.form["targetname"]
    usergroupname = request.form["usergroupname"]

    # Check for mandatory fields
    if not targetname or not usergroupname:
        return "ERROR: The targetname and usergroupname are required ", 417, {
            "Content-Type": "text/plain"}

    # Target and user have to exist in database
    t = get_target(targetname)
    if not t:
        return 'ERROR: No target "' + targetname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    u = get_usergroup(usergroupname)
    if not u:
        return 'ERROR: No usergroup "' + usergroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Check if the given usergroup is a member of the given target
    if not t.usergroupname_in_target(usergroupname):
        return 'ERROR: The usergroup "' + usergroupname + \
            '" is not a member of the target "' + \
            targetname + '" ', 417, {"Content-Type": "text/plain"}

    # Now we can remove the usergroup
    t.rmusergroup(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetname + '" -> ' + e.message, 409, {
            "Content-Type": "text/plain"}

    return 'OK: "' + usergroupname + '" removed from "' + \
        targetname + '"', 200, {"Content-Type": "text/plain"}

# Utils
def get_target(targetname):
    """Return the target with the given targetname"""
    t = db.session.query(target.Target).filter(
        target.Target.targetname == targetname).all()

    # Target must exist in database
    if t:
        return t[0]
    else:
        return False


def get_user(name):
    """Return the user with the given name"""
    u = db.session.query(user.User).filter(
        user.User.name == name).all()

    # User must exist in database
    if u:
        return u[0]
    else:
        return False


def get_usergroup(usergroupname):
    """Return the usergroup with the given usergroupname"""
    g = db.session.query(usergroup.Usergroup).filter(
        usergroup.Usergroup.usergroupname == usergroupname).all()

    # Usergroup must exist in database
    if g:
        return g[0]
    else:
        return False
