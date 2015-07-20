# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import app
from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import target
from app.models_mod import user
from app.models_mod import usergroup


@app.route("/usergroup/list")
def usergroup_list():
    """Return the usergroup list of database"""
    result = []
    query = db.session.query(
        usergroup.Usergroup.usergroupname).order_by(
        usergroup.Usergroup.usergroupname)

    for row in query.all():
        result.append(row[0])

    if not result:
        return "No usergroup in database.", 200, {
            "Content-Type": "text/plain"}

    return "\n".join(result), 200, {"Content-Type": "text/plain"}


@app.route("/usergroup/search/<pattern>")
def usergroup_search(pattern):
    """Return a list of usergroups that match the given pattern"""
    result = []
    query  = db.session.query(usergroup.Usergroup.usergroupname)\
        .filter(usergroup.Usergroup.usergroupname.like("%" + pattern + "%"))

    for row in query.all():
        result.append(row[0])

    if not result:
        return 'No usergroup matching the pattern "' + pattern + \
            '" found.', 200, {"Content-Type": "text/plain"}

    return "\n".join(result), 200, {"Content-Type": "text/plain"}


@app.route("/usergroup/show/<usergroupname>")
def usergroup_show(usergroupname):
    """Return all data about a usergroup"""
    usergroup_data = usergroup.Usergroup.query.filter_by(
        usergroupname=usergroupname).first()

    if usergroup_data is None:
        return 'ERROR: No usergroup with the name "' + usergroupname + \
            '" in the database.', 417, {"Content-Type": "text/plain"}

    return str(usergroup_data), 200, {"Content-Type": "text/plain"}


@app.route("/usergroup/create", methods=["POST"])
def usergroup_create():
    """Add a usergroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    usergroupname = request.form["name"]
    comment = request.form["comment"]

    # Check for required fields
    if not usergroupname:
        return "ERROR: The usergroupname is required ", 417, {
            "Content-Type": "text/plain"}

    # Check unicity for groupname
    query = db.session.query(usergroup.Usergroup.usergroupname)\
        .filter(usergroup.Usergroup.usergroupname.like(usergroupname))

    # Normally only one row
    for row in query.all():
        if str(row[0]) == usergroupname:
            return 'ERROR: The name "' + usergroupname + \
                '" is already used by another user ', \
                417, {"Content-Type": "text/plain"}

    g = usergroup.Usergroup(
        usergroupname=usergroupname,
        comment=comment)
    db.session.add(g)

    # Try to add the usergroup on the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + usergroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + usergroupname + '" -> created', 200, {
        "Content-Type": "text/plain"}


@app.route("/usergroup/edit", methods=["POST"])
def usergroup_edit():
    """Edit a user in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    new_usergroupname = request.form["new_usergroupname"]
    new_comment = request.form["new_comment"]

    toupdate = db.session.query(
        usergroup.Usergroup).filter_by(
        usergroupname=usergroupname)

    # Let's modify only relevent fields
    # Strangely the order is important, have to investigate why
    if new_comment:
        toupdate.update({"comment": new_comment})
    if new_usergroupname:
        toupdate.update(
            {"usergroupname": new_usergroupname})

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + usergroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + usergroupname + '" -> edited', 200, {
        "Content-Type": "text/plain"}


@app.route("/usergroup/del/<usergroupname>")
def usergroup_del(usergroupname):
    """Delete a user in the database"""
    if not usergroupname:
        return "ERROR: The groupname is required ", 417, {
            "Content-Type": "text/plain"}

    # Check if the groupname exists
    query = db.session.query(usergroup.Usergroup.usergroupname)\
        .filter(usergroup.Usergroup.usergroupname.like(usergroupname))

    # Normally only one row
    for row in query.all():
        if str(row[0]) == usergroupname:
            db.session.query(
                usergroup.Usergroup).filter(
                usergroup.Usergroup.usergroupname == usergroupname).delete()

            try:
                db.session.commit()
            except exc.SQLAlchemyError as e:
                return 'ERROR: "' + usergroupname + '" -> ' + \
                    e.message, 409, {"Content-Type": "text/plain"}

            return 'OK: "' + usergroupname + '" -> deleted', 200, {
                "Content-Type": "text/plain"}

    return 'ERROR: No usergroup with the name "' + usergroupname + \
        '" in the database.', 417, {"Content-Type": "text/plain"}


@app.route("/usergroup/adduser", methods=["POST"])
def usergroup_adduser():
    """Add a user in the usergroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    name = request.form["name"]

    # Check for mandatory fields
    if not usergroupname or not name:
        return "ERROR: The usergroupname and name are required ", 417, {
            "Content-Type": "text/plain"}

    # Usergroup and user have to exist in database
    g = get_usergroup(usergroupname)
    if not g:
        return 'ERROR: no usergroup "' + usergroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    u = get_user(name)
    if not u:
        return 'ERROR: no user "' + name + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Now we can add the user
    g.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + usergroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + name + '" added to "' + usergroupname + \
        '"', 200, {"Content-Type": "text/plain"}


@app.route("/usergroup/rmuser", methods=["POST"])
def usergroup_rmuser():
    """Remove a user from the usergroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    name = request.form["name"]

    # Check for mandatory fields
    if not usergroupname or not name:
        return "ERROR: The usergroupname and name are required ", 417, {
            "Content-Type": "text/plain"}

    # Usergroup and user have to exist in database
    g = get_usergroup(usergroupname)
    if not g:
        return 'ERROR: No usergroup "' + usergroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    u = get_user(name)
    if not u:
        return 'ERROR: No user "' + name + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Check if the given user is a member of the given usergroup
    if not g.name_in_usergroup(name):
        return 'ERROR: The user "' + name + \
            '" is not a member of the usergroup "' + \
            usergroupname + '" ', 417, {"Content-Type": "text/plain"}

    # Now we can remove the user
    g.rmuser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + usergroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + name + '" removed from "' + \
        usergroupname + '"', 200, {"Content-Type": "text/plain"}


@app.route("/usergroup/addusergroup", methods=["POST"])
def usergroup_addusergroup():
    """Add a usergroup (subusergroup) in the usergroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    subusergroupname = request.form["subusergroupname"]

    # Check for mandatory fields
    if not usergroupname or not subusergroupname:
        return "ERROR: The usergroupname and subusergroupname are required ", \
            417, {"Content-Type": "text/plain"}

    # Usergroup and subusergroup have to exist in database
    ug = get_usergroup(usergroupname)
    if not ug:
        return 'ERROR: no usergroup "' + usergroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    sug = get_usergroup(subusergroupname)
    if not sug:
        return 'ERROR: no usergroup "' + subusergroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Now we can add the usergroup
    ug.addusergroup(sug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + usergroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + subusergroupname + '" added to "' + \
        usergroupname + '"', 200, {"Content-Type": "text/plain"}


@app.route("/usergroup/rmusergroup", methods=["POST"])
def usergroup_rmusergroup():
    """Remove a usergroup (subusergroup) from the usergroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    subusergroupname = request.form["subusergroupname"]

    # Check for required fields
    if not usergroupname or not subusergroupname:
        return "ERROR: The usergroupname and subusergroupname are required ",
        417, {"Content-Type": "text/plain"}

    # Usergroup and subusergroup have to exist in database
    ug = get_usergroup(usergroupname)
    if not ug:
        return 'ERROR: no usergroup "' + usergroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    sug = get_usergroup(subusergroupname)
    if not sug:
        return 'ERROR: no usergroup "' + subusergroupname + \
            '" in the database ', 417, {"Content-Type": "text/plain"}

    # Now we can remove the usergroup
    ug.rmusergroup(sug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + usergroupname + '" -> ' + \
            e.message, 409, {"Content-Type": "text/plain"}

    return 'OK: "' + subusergroupname + '" removed from "' + \
        usergroupname + '"', 200, {"Content-Type": "text/plain"}

# Utils
def get_usergroup(usergroupname):
    """Return the usergroup with the given usergroupname"""
    g = db.session.query(usergroup.Usergroup).filter(
        usergroup.Usergroup.usergroupname == usergroupname).all()

    # Usergroup must exist in database
    if g:
        return g[0]
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
