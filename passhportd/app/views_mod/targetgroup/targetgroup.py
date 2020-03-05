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
        return  utils.response("No targetgroup in database.", 200)

    return utils.response("\n".join(result), 200)


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
        return utils.response('No targetgroup matching the pattern "' + \
                              pattern + '" found.', 200)

    return utils.response("\n".join(result), 200)


@app.route("/targetgroup/show/<name>")
def targetgroup_show(name):
    """Return all data about a targetgroup"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    targetgroup_data = targetgroup.Targetgroup.query.filter_by(
        name=name).first()

    if targetgroup_data is None:
        return utils.response('ERROR: No targetgroup with the name "' + \
                              name + '" in the database.', 417)

    return utils.response(targetgroup_data.__repr__(), 200)


@app.route("/targetgroup/memberof/<obj>/<name>")
def targetgroup_memberof(obj, name):
    """Return the list of obj this targetgroup is member of"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    data = targetgroup.Targetgroup.query.filter_by(name=name).first()

    if data is None:
        return utils.response('ERROR: No targetgroup with the name "' + name + \
                              '" in the database.', 417)

    return utils.response(str(data.memberof(obj)), 200)


@app.route("/targetgroup/create", methods=["POST"])
def targetgroup_create():
    """Add a targetgroup in the database"""
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
    query = db.session.query(targetgroup.Targetgroup.name)\
        .filter_by(name=name).first()

    if query is not None:
        return utils.response('ERROR: The name "' + name + \
                              '" is already used by another targetgroup ', 417)

    t = targetgroup.Targetgroup(
        name=name,
        comment=comment)
    db.session.add(t)

    # Try to add the targetgroup in the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + \
                              e.message, 409)

    return utils.response('OK: "' + name + '" -> created', 200)


@app.route("/targetgroup/edit", methods=["POST"])
def targetgroup_edit():
    """Edit a targetgroup in the database"""
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
    query = db.session.query(targetgroup.Targetgroup.name).filter_by(
        name=name).first()

    if query is None:
        return utils.response('ERROR: No targetgroup with the name "' + \
                              name + '" in the database.', 417)

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
            return utils.response('ERROR: The name "' + new_name + \
                                  '" is already used by another targetgroup.',\
                                  417)

        to_update.update({"name": new_name})

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + \
                              e.message, 409)

    return utils.response('OK: "' + name + '" -> edited', 200)


@app.route("/targetgroup/delete/<name>")
def targetgroup_delete(name):
    """Delete a targetgroup in the database"""
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    # Check if the name exists
    query = db.session.query(targetgroup.Targetgroup.name)\
        .filter_by(name=name).first()

    if query is None:
        return utils.response('ERROR: No targetgroup with the name "' + \
                              name + '" in the database.', 417)

    tg = db.session.query(
            targetgroup.Targetgroup).filter(
            targetgroup.Targetgroup.name == name)
    tg[0].prepare_delete()
    tg.delete()

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + \
                              e.message, 409)

    return utils.response('OK: "' + name + '" -> deleted', 200)


@app.route("/targetgroup/adduser", methods=["POST"])
def targetgroup_adduser():
    """Add a user in the targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    username = request.form["username"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not username or not targetgroupname:
        return utils.response("ERROR: The username and targetgroupname" + \
                              " are required ", 417)

    # Targetgroup and user have to exist in database
    u = utils.get_user(username)
    if not u:
        return utils.response('ERROR: no user "' + username + \
                              '" in the database ', 417)

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return utils.response('ERROR: no targetgroup "' + targetgroupname + \
                              '" in the database ', 417)

    # Now we can add the user
    tg.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + targetgroupname + '" -> ' + \
                              e.message, 409)

    utils.notif("User " + username + " is now in " + targetgroupname + ".", 
                "[PaSSHport] " + username + " joins " + targetgroupname )
    return utils.response('OK: "' + username + '" added to "' + \
                          targetgroupname + '"', 200)


@app.route("/targetgroup/rmuser", methods=["POST"])
def targetgroup_rmuser():
    """Remove a user from the targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    username = request.form["username"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not username or not targetgroupname:
        return utils.response("ERROR: The username and targetgroupname" + \
                              " are required ", 417)

    # User and targetgroup have to exist in database
    u = utils.get_user(username)
    if not u:
        return utils.response('ERROR: no user "' + username + \
                              '" in the database ', 417)

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return utils.response('ERROR: no targetgroup "' + targetgroupname + \
                              '" in the database ', 417)

    # Check if the given user is a member of the given targetgroup
    if not tg.username_in_targetgroup(username):
        return utils.response('ERROR: The user "' + username + \
                              '" is not a member of the targetgroup "' + \
                              targetgroupname + '" ', 417)

    # Now we can remove the user
    tg.rmuser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + targetgroupname + '" -> ' + \
                              e.message, 409)

    utils.notif("User " + username + " has been removed from " + targetgroupname + ".", 
                "[PaSSHport] " + username + " removed from " + targetgroupname )
    return utils.response('OK: "' + username + '" removed from "' + \
                          targetgroupname + '"', 200)


@app.route("/targetgroup/addtarget", methods=["POST"])
def targetgroup_addtarget():
    """Add a target in the targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    targetname = request.form["targetname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not targetname or not targetgroupname:
        return utils.response("ERROR: The targetname and targetgroupname" + \
                              " are required ", 417)

    # Target and targetgroup have to exist in database
    t = utils.get_target(targetname)
    if not t:
        return utils.response('ERROR: no target "' + targetname + \
                              '" in the database ', 417)

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return utils.response('ERROR: no targetgroup "' + targetgroupname + \
                              '" in the database ', 417)

    # Now we can add the target
    tg.addtarget(t)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + targetgroupname + '" -> ' + \
                              e.message, 409)
 
    utils.notif("Users from " + targetgroupname+ " can now access to " + targetame + ".", 
                "[PaSSHport] " + targetname + " access granted to " + targetgroupname )
    return utils.response('OK: "' + targetname + '" added to "' + \
                          targetgroupname + '"', 200)


@app.route("/targetgroup/rmtarget", methods=["POST"])
def targetgroup_rmtarget():
    """Remove a target from the targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    targetname = request.form["targetname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not targetname or not targetgroupname:
        return utils.response("ERROR: The targetname and targetgroupname" + \
                              " are required ", 417)

    # Target and targetgroup have to exist in database
    t = utils.get_target(targetname)
    if not t:
        return utils.response('ERROR: No target "' + targetname + \
                              '" in the database ', 417)

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return utils.response('ERROR: No targetgroup "' + targetgroupname + \
                              '" in the database ', 417)

    # Check if the given target is a member of the given targetgroup
    if not tg.targetname_in_targetgroup(targetname):
        return utils.response('ERROR: The target "' + targetname + \
                              '" is not a member of the targetgroup "' + \
                              tg.show_name() + '" ', 417)

    # Now we can remove the target
    tg.rmtarget(t)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + targetgroupname + '" -> ' + \
                              e.message, 409)

    utils.notif("Users from " + targetgroupname+ " can not access to " + \
                                                     targetame + "anymore.",
                "[PaSSHport] " + targetname + " removed from " + \
                                                        targetgroupname )
    return utils.response('OK: "' + targetname + '" removed from "' + \
                          targetgroupname + '"', 200)


@app.route("/targetgroup/addusergroup", methods=["POST"])
def targetgroup_addusergroup():
    """Add a usergroup in the targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not usergroupname or not targetgroupname:
        return utils.response("ERROR: The usergroupname and " + \
                              "targetgroupname are required ", 417)

    # Usergroup and targetgroup have to exist in database
    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return utils.response('ERROR: no usergroup "' + usergroupname + \
                              '" in the database ', 417)

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return utils.response('ERROR: no targetgroup "' + targetgroupname + \
                              '" in the database ', 417)

    # Now we can add the usergroup
    tg.addusergroup(ug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + targetgroupname + '" -> ' + \
                              e.message, 409)

    utils.notif("Users from " + usergroupname + \
               " can now access to the targets from " + targetgroupame + ".", 
                "[PaSSHport] " + usergroupname + " added to " + targetgroupname)
    return utils.response('OK: "' + usergroupname + '" added to "' + \
                          targetgroupname + '"', 200)


@app.route("/targetgroup/rmusergroup", methods=["POST"])
def targetgroup_rmusergroup():
    """Remove a usergroup from the targetgroup in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not usergroupname or not targetgroupname:
        return utils.response("ERROR: The usergroupname and " + \
                              "targetgroupname are required ", 417)

    # Usergroup and targetgroup have to exist in database
    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return utils.response('ERROR: no usergroup "' + usergroupname + \
                              '" in the database ', 417)

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return utils.response('ERROR: no targetgroup "' + targetgroupname + \
                              '" in the database ', 417)

    # Check if the given usergroup is a member of the given targetgroup
    if not tg.usergroupname_in_targetgroup(usergroupname):
        return utils.response('ERROR: The usergroup "' + usergroupname + \
                              '" is not a member of the targetgroup "' + \
                              targetgroupname + '" ', 417)

    # Now we can remove the usergroup
    tg.rmusergroup(ug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + targetgroupname + '" -> ' + \
                              e.message, 409)

    utils.notif("Users from " + usergroupname + \
               " lost access to the targets from " + targetgroupame + ".", 
               "[PaSSHport] " + usergroupname + " removed from " + \
                                                          targetgroupname)
    return utils.response('OK: "' + usergroupname + '" removed from "' + \
                          targetgroupname + '"', 200)


@app.route("/targetgroup/addtargetgroup", methods=["POST"])
def targetgroup_addtargetgroup():
    """Add a targetgroup (subtargetgroup) in the targetgroup
    in the database
    """
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    subtargetgroupname = request.form["subtargetgroupname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not subtargetgroupname or not targetgroupname:
        return utils.response("ERROR: The subtargetgroupname and "
                              "targetgroupname are required ", 417)

    # Subtargetgroup and targetgroup have to exist in database
    stg = utils.get_targetgroup(subtargetgroupname)
    if not stg:
        return utils.response('ERROR: no targetgroup "' + \
                              subtargetgroupname + '" in the database ', 417)

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return utils.response('ERROR: no targetgroup "' + targetgroupname + \
                              '" in the database ', 417)

    # Now we can add the subtargetgroup
    if not tg.addtargetgroup(stg):
        if tg == stg:
            return utils.response("ERROR: impossible to add a targetgroup" + \
                                  " into itself.", 417)

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + targetgroupname + '" -> ' + \
                              e.message, 409)

    utils.notif("Users from " + subtargetgroupname + \
               " can access to the targets from " + targetgroupame + ".", 
               "[PaSSHport] " + subtargetgroupname + " added to " + \
                                                          targetgroupname)
    return utils.response('OK: "' + subtargetgroupname + '" added to "' + \
                          targetgroupname + '"', 200)


@app.route("/targetgroup/rmtargetgroup", methods=["POST"])
def targetgroup_rmtargetgroup():
    """Remove a targetgroup (subtargetgroup) from the targetgroup
    in the database
    """
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    subtargetgroupname = request.form["subtargetgroupname"]
    targetgroupname = request.form["targetgroupname"]

    # Check for required fields
    if not subtargetgroupname or not targetgroupname:
        return utils.response("ERROR: The subtargetgroupname and " + \
                              "targetgroupname are required ", 417)

    # Subtargetgroup and targetgroup have to exist in database
    stg = utils.get_targetgroup(subtargetgroupname)
    if not stg:
        return utils.response('ERROR: no targetgroup "' + \
                              subtargetgroupname + '" in the database ', 417)

    tg = utils.get_targetgroup(targetgroupname)
    if not tg:
        return utils.response('ERROR: no targetgroup "' + targetgroupname + \
                              '" in the database ', 417)

    # Check if the given subtargetgroup is a member of the given targetgroup
    if not tg.subtargetgroupname_in_targetgroup(subtargetgroupname):
        return utils.response('ERROR: The subtargetgroup "' + \
                              subtargetgroupname + '" is not a member of " + \
                              the targetgroup "' + targetgroupname + '" ', 417)

    # Now we can remove the subtargetgroup
    tg.rmtargetgroup(stg)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + targetgroupname + '" -> ' + \
                              e.message, 409)

    utils.notif("Users from " + subtargetgroupname + \
               " removed access to " + targetgroupame + ".", 
               "[PaSSHport] " + subtargetgroupname + " removed from " + \
                                                          targetgroupname)
    return utils.response('OK: "' + subtargetgroupname + '" added to "' + \
    return utils.response('OK: "' + subtargetgroupname + '" removed from "' + \
                          targetgroupname + '"', 200)


@app.route("/targetgroup/access/<name>")
def targetgroup_access(name):
    """Return all the targets accessible if you're in this targetgroup"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    data = targetgroup.Targetgroup.query.filter_by(name=name).first()

    if data is None:
        return utils.response('ERROR: No targetgroup with the name "' + name + \
                              '" in the database.', 417)

    return utils.response(str(data.accessible_target_list(style="names")), 200)

