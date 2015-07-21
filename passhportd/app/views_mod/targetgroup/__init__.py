# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import app, db
from flask import request
from app.models_mod import targetgroup
from app.models_mod import target
from app.models_mod import user
from app.models_mod import usergroup


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
        return "No targetgroup in database.", 200, {
            "Content-Type": "text/plain"}

    return "\n".join(result), 200, {"Content-Type": "text/plain"}


@app.route("/targetgroup/search/<pattern>")
def targetgroup_search(pattern):
    """Return a list of targetgroups that match the given pattern"""
    result = []
    query = db.session.query(
        targetgroup.Targetgroup.name) .filter(
        targetgroup.Targetgroup.name.like(
            "%" +
            pattern +
            "%"))

    for row in query.all():
        result.append(str(row[0]))

    if not result:
        return 'No targetgroup matching the pattern "' + pattern + \
            '" found.', 200, {"Content-Type": "text/plain"}

    return "\n".join(result), 200, {"Content-Type": "text/plain"}


@app.route("/targetgroup/show/<name>")
def targetgroup_show(name):
    """Return all data about a targetgroup"""
    targetgroup_data = targetgroup.Targetgroup.query.filter_by(
        name=name).first()

    if targetgroup_data is None:
        return 'ERROR: No targetgroup with the name "' + name + \
            '" in the database.', 417, {"Content-Type": "text/plain"}

    return str(targetgroup_data), 200, {"Content-Type": "text/plain"}


@app.route("/targetgroup/create", methods=["POST"])
def targetgroup_create():
    """Add a targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    name = request.form["name"]
    comment = request.form["comment"]

    # Check for mandatory fields
    if not name:
        return "ERROR: The name is required ", 417, {
            "Content-Type": "text/plain"}

    # Check unicity for name
    query = db.session.query(targetgroup.Targetgroup.name)\
        .filter(targetgroup.Targetgroup.name.like(name))

    # Normally only one row
    for row in query.all():
        if str(row[0]) == name:
            return 'ERROR: The name "' + name + \
                '" is already used by another targetgroup ', \
                417, {"Content-Type": "text/plain"}

    t = targetgroup.Targetgroup(
        name=name,
        comment=comment)
    db.session.add(t)

    # Try to add the targetgroup in the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + name + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + name + '" -> created', 200, {"Content-Type": "text/plain"}


@app.route("/targetgroup/edit", methods=["POST"])
def targetgroup_edit():
    """Edit a targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    name = request.form["name"]
    new_name = request.form["new_name"]
    new_comment = request.form["new_comment"]

    toupdate = db.session.query(
        targetgroup.Targetgroup).filter_by(
        name=name)

    # Let's modify only relevent fields
    if new_comment:
        toupdate.update({"comment": str(new_comment)})
    if new_name:
        toupdate.update(
            {"name": str(new_name)})

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + name + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + name + '" -> edited' + \
        "\n", 200, {"Content-Type": "text/plain"}


@app.route("/targetgroup/delete/<name>")
def targetgroup_delete(name):
    """Delete a targetgroup in the database"""
    if not name:
        return "ERROR: The name is required ", 417, {
            "Content-Type": "text/plain"}

    # Check if the name exists
    query = db.session.query(targetgroup.Targetgroup.name)\
        .filter(targetgroup.Targetgroup.name.like(name))

    # Normally only one row
    for row in query.all():
        if str(row[0]) == name:
            db.session.query(
                targetgroup.Targetgroup).filter(
                targetgroup.Targetgroup.name == name)\
                .delete()

            try:
                db.session.commit()
            except exc.SQLAlchemyError:
                return 'ERROR: "' + name + '" -> ' + \
                    e.message, 409, {"Content-Type": "text/plain"}

            return 'OK: "' + name + '" -> deleted', 200, {
                "Content-Type": "text/plain"}

    return 'ERROR: No targetgroup with the name "' + name + \
        '" in the database.', 417, {"Content-Type": "text/plain"}

@app.route("/targetgroup/adduser", methods=["POST"])
def targetgroup_adduser():
    """Add a user in the targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetgroupname = request.form["targetgroupname"]
    username = request.form["username"]

    # Check for required fields
    if not targetgroupname or not username:
        return "ERROR: The targetgroupname and username are required ", 417, {
            "Content-Type": "text/plain"}

    # Targetgroup and user have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    u = get_user(username)
    if not u:
        return 'ERROR: no user "' + username + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Now we can add the user
    tg.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + username + '" added to "' + targetgroupname + \
        '"', 200, {"Content-Type": "text/plain"}


@app.route("/targetgroup/rmuser", methods=["POST"])
def targetgroup_rmuser():
    """Remove a user from the targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetgroupname = request.form["targetgroupname"]
    username = request.form["username"]

    # Check for required fields
    if not targetgroupname or not username:
        return "ERROR: The targetgroupname and username are required ", 417, {
            "Content-Type": "text/plain"}

    # Targetgroup and user have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    u = get_user(username)
    if not u:
        return 'ERROR: no user "' + username + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Now we can remove the user
    tg.rmuser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + username + '" removed from "' + \
        targetgroupname + '"', 200, {"Content-Type": "text/plain"}

@app.route("/targetgroup/addtarget", methods=["POST"])
def targetgroup_addtarget():
    """Add a target in the targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetname = request.form["targetname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for mandatory fields
    if not targetname or not targetgroupname:
        return "ERROR: The targetname and targetgroupname are required ",
        417, {"Content-Type": "text/plain"}

    # Targetgroup and target have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    t = get_target(targetname)
    if not t:
        return 'ERROR: no target "' + targetname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Now we can add the target
    tg.addtarget(t)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + targetname + '" added to "' + \
        targetgroupname + '"', 200, {"Content-Type": "text/plain"}


@app.route("/targetgroup/rmtarget", methods=["POST"])
def targetgroup_rmtarget():
    """Remove a target from the targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetname = request.form["targetname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not targetname or not targetgroupname:
        return "ERROR: The targetname and targetgroupname are required ",
        417, {"Content-Type": "text/plain"}

    # Targetgroup and target have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: No targetgroup "' + targetgroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    t = get_target(targetname)
    if not t:
        return 'ERROR: No target "' + targetname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Check if the given target is a member of the given targetgroup
    if not tg.targetname_in_targetgroup(targetname):
        return 'ERROR: The target "' + target + \
            '" is not a member of the targetgroup "' + \
            targetgroupname + '" ', 417, {"Content-Type": "text/plain"}

    # Now we can remove the target
    tg.rmtarget(t)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + targetname + '" removed from "' + \
        targetgroupname + '"', 200, {"Content-Type": "text/plain"}

@app.route("/targetgroup/addusergroup", methods=["POST"])
def targetgroup_addusergroup():
    """Add a usergroup in the targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetgroupname = request.form["targetgroupname"]
    usergroupname = request.form["usergroupname"]

    # Check for required fields
    if not targetgroupname or not usergroupname:
        return "ERROR: The targetgroupname and usergroupname are required ",
        417, {"Content-Type": "text/plain"}

    # Targetgroup and usergroup have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    ug = get_usergroup(usergroupname)
    if not ug:
        return 'ERROR: no usergroup "' + usergroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Now we can add the usergroup
    tg.addusergroup(ug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + usergroupname + '" added to "' + \
        targetgroupname + '"', 200, {"Content-Type": "text/plain"}


@app.route("/targetgroup/rmusergroup", methods=["POST"])
def targetgroup_rmusergroup():
    """Remove a usergroup from the targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetgroupname = request.form["targetgroupname"]
    usergroupname = request.form["usergroupname"]

    # Check for required fields
    if not targetgroupname or not usergroupname:
        return "ERROR: The targetgroupname and usergroupname are required ",
        417, {"Content-Type": "text/plain"}

    # Targetgroup and usergroup have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    ug = get_usergroup(usergroupname)
    if not ug:
        return 'ERROR: no usergroup "' + usergroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Now we can remove the usergroup
    tg.rmusergroup(ug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + usergroupname + '" removed from "' + \
        targetgroupname + '"', 200, {"Content-Type": "text/plain"}


@app.route("/targetgroup/addtargetgroup", methods=["POST"])
def targetgroup_addtargetgroup():
    """Add a targetgroup (subtargetgroup) in the targetgroup
    in the database
    """
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetgroupname = request.form["targetgroupname"]
    subtargetgroupname = request.form["subtargetgroupname"]

    # Check for required fields
    if not targetgroupname or not subtargetgroupname:
        return "ERROR: The targetgroupname and subtargetgroupname "
        "are required ", 417, {"Content-Type": "text/plain"}

    # Targetgroup and subtargetgroup have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    subtg = get_targetgroup(subtargetgroupname)
    if not subtg:
        return 'ERROR: no targetgroup "' + subtargetgroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Now we can add the targetgroup
    tg.addtargetgroup(subtg)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + subtargetgroupname + '" added to "' + \
        targetgroupname + '"', 200, {"Content-Type": "text/plain"}


@app.route("/targetgroup/rmtargetgroup", methods=["POST"])
def targetgroup_rmtargetgroup():
    """Remove a targetgroup (subtargetgroup) from the targetgroup
    in the database
    """
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetgroupname = request.form["targetgroupname"]
    subtargetgroupname = request.form["subtargetgroupname"]

    # Check for required fields
    if not targetgroupname or not subtargetgroupname:
        return "ERROR: The targetgroupname and subtargetgroupname "
        "are required ", 417, {"Content-Type": "text/plain"}

    # Targetgroup and subtargetgroup have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    subtg = get_targetgroup(subtargetgroupname)
    if not subtg:
        return 'ERROR: no targetgroup "' + subtargetgroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Now we can remove the targetgroup
    tg.rmtargetgroup(subtg)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetgroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + subtargetgroupname + '" removed from "' + \
        targetgroupname + '"', 200, {"Content-Type": "text/plain"}

# Utils
def get_user(name):
    """Return the user with the given name"""
    u = db.session.query(user.User).filter(
        user.User.name == name).all()

    # User must exist in database
    if u:
        return u[0]
    else:
        return False


def get_usergroup(name):
    """Return the usergroup with the given usergroupname"""
    ug = db.session.query(usergroup.Usergroup).filter(
        usergroup.Usergroup.name == name).all()

    # Usergroup must exist in database
    if ug:
        return ug[0]
    else:
        return False


def get_target(name):
    """Return the target with the given name"""
    t = db.session.query(target.Target).filter(
        target.Target.name == name).all()

    # Target must exist in database
    if t:
        return t[0]
    else:
        return False


def get_targetgroup(name):
    """Return the targetgroup with the given name"""
    tg = db.session.query(targetgroup.Targetgroup).filter(
        targetgroup.Targetgroup.name == name).all()

    # Targetgroup must exist in database
    if tg:
        return tg[0]
    else:
        return False
