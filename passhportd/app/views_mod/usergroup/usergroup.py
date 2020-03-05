# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import user, usergroup
from . import api

from .. import utilities as utils


@app.route("/usergroup/list")
def usergroup_list():
    """Return the usergroup list of database"""
    result = []
    query = db.session.query(
        usergroup.Usergroup.name).order_by(
        usergroup.Usergroup.name)

    for row in query.all():
        result.append(row[0])

    if not result:
        return utils.response("No usergroup in database.", 200)

    return utils.response("\n".join(result), 200)


@app.route("/usergroup/search/<pattern>")
def usergroup_search(pattern):
    """Return a list of usergroups that match the given pattern"""
    result = []
    query  = db.session.query(usergroup.Usergroup.name)\
        .filter(usergroup.Usergroup.name.like("%" + pattern + "%"))

    for row in query.all():
        result.append(row[0])

    if not result:
        return utils.response('No usergroup matching the pattern "' + \
                              pattern + '" found.', 200)

    return utils.response("\n".join(result), 200)


@app.route("/usergroup/show/<name>")
def usergroup_show(name):
    """Return all data about a usergroup"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    usergroup_data = usergroup.Usergroup.query.filter_by(name=name).first()

    if usergroup_data is None:
        return utils.response('ERROR: No usergroup with the name "' + name + \
                              '" in the database.', 417)

    return utils.response(str(usergroup_data), 200)


@app.route("/usergroup/memberof/<obj>/<name>")
def usergroup_memberof(obj, name):
    """Return the list of obj this usergroup is member of"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    usergroup_data = usergroup.Usergroup.query.filter_by(name=name).first()

    if usergroup_data is None:
        return utils.response('ERROR: No usergroup with the name "' + name + \
                              '" in the database.', 417)

    return utils.response(str(usergroup_data.memberof(obj)), 200)

    
@app.route("/usergroup/access/<name>")
def usergroup_access(name):
    """Return all the targets accessible if you're in this usergroup"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    usergroup_data = usergroup.Usergroup.query.filter_by(name=name).first()

    if usergroup_data is None:
        return utils.response('ERROR: No usergroup with the name "' + name + \
                              '" in the database.', 417)

    return utils.response(str(usergroup_data.accessible_target_list()), 200)


@app.route("/usergroup/create", methods=["POST"])
def usergroup_create():
    """Add a usergroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    name = request.form["name"]
    comment = request.form["comment"]

    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    # Check unicity for name
    query = db.session.query(usergroup.Usergroup.name)\
        .filter_by(name=name).first()

    if query is not None:
        return utils.response('ERROR: The name "' + name + \
                              '" is already used by another usergroup ', 417)

    g = usergroup.Usergroup(
        name=name,
        comment=comment)
    db.session.add(g)

    # Try to add the usergroup on the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + \
                              e.message, 409)

    return utils.response('OK: "' + name + '" -> created', 200)


@app.route("/usergroup/edit", methods=["POST"])
def usergroup_edit():
    """Edit a user in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    name = request.form["name"]
    new_name = request.form["new_name"]
    new_comment = request.form["new_comment"]

    # Check required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    # Check if the name exists in the database
    query = db.session.query(usergroup.Usergroup.name).filter_by(
        name=name).first()

    if query is None:
        return utils.response('ERROR: No usergroup with the name "' + name + \
                              '" in the database.', 417)

    to_update = db.session.query(
        usergroup.Usergroup.name).filter_by(
        name=name)

    # Let's modify only relevent fields
    # Strangely the order is important, have to investigate why
    if new_comment:
        # This specific string allows admins to remove old comments
        if new_comment == "PASSHPORTREMOVECOMMENT":
            new_comment = ""
        to_update.update({"comment": new_comment})
    if new_name:
        # Check unicity for name
        query = db.session.query(usergroup.Usergroup.name)\
            .filter_by(name=new_name).first()

        if query is not None and new_name != query.name:
            return utils.response('ERROR: The name "' + new_name + \
                                  '" is already used by another usergroup ',
                                  417)

        to_update.update({"name": new_name})

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + \
                              e.message, 409)

    return utils.response('OK: "' + name + '" -> edited', 200)


@app.route("/usergroup/delete/<name>")
def usergroup_delete(name):
    """Delete a usergroup in the database"""
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    # Check if the name exists
    query = db.session.query(
                usergroup.Usergroup).filter(
                usergroup.Usergroup.name == name)

    if query is None:
        return utils.response('ERROR: No usergroup with the name "' + name + \
                              '" in the database.', 417)
    
    #Normaly there will be only one element with that name
    ug = query[0]
    ug.prepare_delete()
    query.delete()

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + \
                              e.message, 409)

    return utils.response('OK: "' + name + '" -> deleted', 200)


@app.route("/usergroup/adduser", methods=["POST"])
def usergroup_adduser():
    """Add a user in the usergroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    username = request.form["username"]
    usergroupname = request.form["usergroupname"]

    # Check for required fields
    if not username or not usergroupname:
        return utils.response("ERROR: The username and usergroupname " + \
                              "are required ", 417)

    # User and usergroup have to exist in database
    u = utils.get_user(username)
    if not u:
        return utils.response('ERROR: no user "' + username + \
                              '" in the database ', 417)

    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return utils.response('ERROR: no usergroup "' + usergroupname + \
                              '" in the database ', 417)

    # Now we can add the user
    ug.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + usergroupname + '" -> ' + \
                              e.message, 409)

    utils.notif(username + " added to " + usergroupame + ".\n" + \
            "He can now access to: \n" + usergroupame.accessible_target_list(),
            "[PaSSHport] " + username + " added to " + usergroupname)
    return utils.response('OK: "' + username + '" added to "' + \
                          usergroupname + '"', 200)


@app.route("/usergroup/rmuser", methods=["POST"])
def usergroup_rmuser():
    """Remove a user from the usergroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    username = request.form["username"]
    usergroupname = request.form["usergroupname"]

    # Check for required fields
    if not username or not usergroupname:
        return utils.response("ERROR: The username and usergroupname are " + \
                              "required ", 417)

    # User and usergroup have to exist in database
    u = utils.get_user(username)
    if not u:
        return utils.response('ERROR: No user "' + username + \
                              '" in the database ', 417)

    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return utils.response('ERROR: No usergroup "' + usergroupname + \
                              '" in the database ', 417)

    # Check if the given user is a member of the given usergroup
    if not ug.username_in_usergroup(username):
        return utils.response('ERROR: The user "' + username + \
                              '" is not a member of the usergroup "' + \
                              usergroupname + '" ', 417)

    # Now we can remove the user
    ug.rmuser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + usergroupname + '" -> ' + \
                              e.message, 409)

    utils.notif(username + " removed from " + usergroupam2Ye + ".",
            "[PaSSHport] " + username + " removed from " + usergroupname)
    return utils.response('OK: "' + username + '" removed from "' + \
                          usergroupname + '"', 200)


@app.route("/usergroup/addmanager", methods=["POST"])
def usergroup_addmanager():
    """Add a manager in the usergroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    username = request.form["username"]
    usergroupname = request.form["usergroupname"]

    # Check for required fields
    if not username or not usergroupname:
        return utils.response("ERROR: The username and usergroupname " + \
                              "are required ", 417)

    # User and usergroup have to exist in database
    u = utils.get_user(username)
    if not u:
        return utils.response('ERROR: no user "' + username + \
                              '" in the database ', 417)

    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return utils.response('ERROR: no usergroup "' + usergroupname + \
                              '" in the database ', 417)

    # Now we can add the user
    ug.addmanager(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + usergroupname + '" -> ' + \
                              e.message, 409)

    utils.notif(username + " is now manager of " + usergroupam2Ye + ".",
            "[PaSSHport] " + username + " promoted manager of " + usergroupname)
    return utils.response('OK: "' + username + '" is manager of "' + \
                          usergroupname + '"', 200)


@app.route("/usergroup/rmmanager", methods=["POST"])
def usergroup_rmmanager():
    """Remove a manager from the usergroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    username = request.form["username"]
    usergroupname = request.form["usergroupname"]

    # Check for required fields
    if not username or not usergroupname:
        return utils.response("ERROR: The username and usergroupname are " + \
                              "required ", 417)

    # User and usergroup have to exist in database
    u = utils.get_user(username)
    if not u:
        return utils.response('ERROR: No user "' + username + \
                              '" in the database ', 417)

    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return utils.response('ERROR: No usergroup "' + usergroupname + \
                              '" in the database ', 417)

    # Check if the given user is a manager of the given usergroup
    if not ug.manager_in_usergroup(username):
        return utils.response('ERROR: The user "' + username + \
                              '" is not a manager of the usergroup "' + \
                              usergroupname + '" ', 417)

    # Now we can remove the user
    ug.rmmanager(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + usergroupname + '" -> ' + \
                              e.message, 409)

    return utils.response('OK: "' + username + \
                          '" is not anymore manager of "' + \
                          usergroupname + '"', 200)


@app.route("/usergroup/ismanager/<name>/<user>", methods=["GET"])
def user_ismanager(name, user):
    """Return True if the user is superadmin"""
    usergroupobj = utils.check_usergroup_get(request, name)
    if not usergroupobj:
        return utils.response("ERROR: The request is not correct", 417)

    return utils.response(str(usergroupobj.name_is_manager(user)), 200)
    

@app.route("/usergroup/addusergroup", methods=["POST"])
def usergroup_addusergroup():
    """Add a usergroup (subusergroup) in the usergroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    subusergroupname = request.form["subusergroupname"]
    usergroupname = request.form["usergroupname"]

    # Check for required fields
    if not subusergroupname or not usergroupname:
        return utils.response("ERROR: The subusergroupname and " + \
                              "usergroupname are required ", 417)

    # Subsergroup and usergroup have to exist in database
    sug = utils.get_usergroup(subusergroupname)
    if not sug:
        return utils.response('ERROR: no usergroup "' + subusergroupname + \
                              '" in the database ', 417)

    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return utils.response('ERROR: no usergroup "' + usergroupname + \
                              '" in the database ', 417)

    # Now we can add the usergroup (impossible to add a usergroup to itself)
    if not ug.addusergroup(sug):
        if sug == ug:
            return utils.response("ERROR: sorry you can't add " + \
                                  "a usergroup to itself" , 417)

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + usergroupname + '" -> ' + \
                              e.message, 409)

    return utils.response('OK: "' + subusergroupname + '" added to "' + \
                          usergroupname + '"', 200)


@app.route("/usergroup/rmusergroup", methods=["POST"])
def usergroup_rmusergroup():
    """Remove a usergroup (subusergroup) from the usergroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    subusergroupname = request.form["subusergroupname"]

    # Check for required fields
    if not usergroupname or not subusergroupname:
        return utils.response("ERROR: The usergroupname and " + \
                              "subusergroupname are required ", 417)

    # Usergroup and subusergroup have to exist in database
    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return utils.response('ERROR: no usergroup "' + usergroupname + \
                              '" in the database ', 417)

    sug = utils.get_usergroup(subusergroupname)
    if not sug:
        return utils.response('ERROR: no usergroup "' + subusergroupname + \
                              '" in the database ', 417)

    # Check if the given subusergroup is a member of the given usergroup
    if not ug.subusergroupname_in_usergroup(subusergroupname):
        return utils.response('ERROR: The subusergroup "' + \
                              subusergroupname + '" is not a member of ' + \
                              'the usergroup "' + usergroupname + '" ', 417)

    # Now we can remove the subusergroup
    ug.rmusergroup(sug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + usergroupname + '" -> ' + \
                              e.message, 409)

    return utils.response('OK: "' + subusergroupname + '" removed from "' + \
                          usergroupname + '"', 200)
