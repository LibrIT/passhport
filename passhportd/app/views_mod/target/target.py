# -*-coding:Utf-8 -*-
from flask import request
from sqlalchemy import exc, and_
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import user, target, usergroup, exttargetaccess, passentry
from . import api
from subprocess import Popen, PIPE
from datetime import datetime, timedelta
import os
import config

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
        return utils.response("No target in database.", 200)

    return utils.response("\n".join(result), 200)


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
        return utils.response('No target matching the pattern "' + pattern + \
                              '" found.', 200)

    return utils.response("\n".join(result), 200)


@app.route("/target/memberof/<obj>/<name>")
def target_memberof(obj, name):
    """Return the list of obj this target is member of (obj shoud be tg)"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    target_data = target.Target.query.filter_by(name=name).first()

    if target_data is None:
        return utils.response('ERROR: No target with the name "' + name + \
                              '" in the database.', 417)

    return utils.response(str(target_data.memberof(obj)), 200)


@app.route("/target/checkaccess/<pattern>")
def target_checkaccess(pattern):
    """Check SSH connection for each target with a name or hostname that 
       match the pattern. And return the result for each target"""
    result = []
    query  = db.session.query(target.Target) \
        .filter(target.Target.hostname.like("%" + pattern + "%") | \
        target.Target.name.like("%" + pattern + "%")) \
        .order_by(target.Target.name).all()

    for targetobj in query:
        hostname = targetobj.hostname
        login = targetobj.login
        port = targetobj.port
        sshoptions = targetobj.sshoptions
        #Check minimal infos
        if hostname:
            if not login:
                login = "root"
            if not port:
                port = 22
            if not sshoptions:
                sshoptions = ""
            # Need to trick ssh: we don't want to check fingerprints
            # neither to interfer with the local fingerprints file
            sshcommand = "ssh -p" + str(port) + \
                    " " + login + "@" + hostname + \
                    " " + sshoptions + " " \
                    "-o PasswordAuthentication=no " + \
                    "-o UserKnownHostsFile=/dev/null " + \
                    "-o StrictHostKeyChecking=no " + \
                    "-o ConnectTimeout=10 " + \
                    "echo OK"

            # Try to connect and get the result
            r = os.system(sshcommand)
            if r == 0:
                result.append("OK:   " + hostname + "\t" + \
                        targetobj.name)
            else:
                result.append("ERROR:" + hostname + "\t" + \
                        targetobj.name + "\tError with this ssh command " + \
                        "(return code -> " + str(r) + "): " + sshcommand)

    if not result:
        return utils.response('No target hostname matching the pattern "' + \
                              pattern + '" found.', 200)

    return utils.response("\n".join(result), 200)


@app.route("/target/show/<name>")
def target_show(name):
    """Return all data about a target"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    target_data = target.Target.query.filter_by(name=name).first()

    if target_data is None:
        return utils.response('ERROR: No target with the name "' + name + \
                              '" in the database.', 417)

    return utils.response(str(target_data), 200)


@app.route("/target/port/<name>")
def target_port(name):
    """Return port related to a target"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    target_data = target.Target.query.filter_by(name=name).first()

    if target_data is None:
        return utils.response('ERROR: No target with the name "' + name + \
                              '" in the database.', 417)

    port = target_data.port

    # If there is no port declared, we assume it's 22
    if port is None:
        app.logger.warning("No port set on " + name + ", 22 is used")
        port = "22"
    else:
        port = str(port).replace(" ","")
    
    return utils.response(port, 200)


@app.route("/target/login/<name>")
def target_login(name):
    """Return login related to a target"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    target_data = target.Target.query.filter_by(name=name).first()

    if target_data is None:
        return utils.response('ERROR: No target with the name "' + name + \
                              '" in the database.', 417)

    login = target_data.login

    # If there is no user declared, we assume it's root
    if login is None:
        app.logger.warning("No login set on " + name + ", root is used")
        login = "root"
    else:
        login = str(login).replace(" ","")
    
    return utils.response(login, 200)


@app.route("/target/sshoptions/<name>")
def target_options(name):
    """Return options related to a target"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    target_data = target.Target.query.filter_by(name=name).first()

    if target_data is None:
        return utils.response('ERROR: No target with the name "' + name + \
                              '" in the database.', 417)

    return utils.response(str(target_data.sshoptions), 200)


@app.route("/target/create", methods=["POST"])
def target_create():
    """Add a target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    name = request.form["name"].replace(" ", "")
    hostname = request.form["hostname"].replace(" ", "")
    targettype = request.form["targettype"].replace(" ", "")
    login = request.form["login"].replace(" ", "")
    port = request.form["port"].replace(" ", "")
    sshoptions = request.form["sshoptions"]
    comment = request.form["comment"]
    changepwd = request.form["changepwd"].replace(" ", "")
    sessiondur = ""
    if "sessiondur" in request.form:
        if utils.is_number(request.form["sessiondur"]):
            app.logger.error(request.form["sessiondur"])
            sessiondur = int(request.form["sessiondur"].replace(" ", ""))*60

    # Check for required fields
    if not name or not hostname:
        return utils.response("ERROR: The name and hostname are" + \
                              " required", 417)

    if not targettype:
        targettype = "ssh"

    if not login:
        login = "root"

    if not port:
        if targettype == "ssh":
            port = 22
        elif targettype == "mysql":
            port = 3306    
        elif targettype == "postgresql":
            port = 5432
        elif targettype == "oracle" : 
            port = 1521

    if not changepwd:
        changepwd = False
    elif changepwd == "True":
        changepwd = True
    else:
        changepwd=False

    if not sessiondur:
        sessiondur = 60*int(config.DB_SESSIONS_TO)

    # Check unicity for name
    query = db.session.query(target.Target.name)\
        .filter_by(name=name).first()

    if query is not None:
        return utils.response('ERROR: The name "' + name + \
                              '" is already used by another target ', 417)


    t = target.Target(
        name       = name,
        hostname   = hostname,
        targettype = targettype,
        login      = login,
        port       = port,
        sshoptions = sshoptions,
        comment    = comment,
        changepwd  = changepwd,
        sessiondur = sessiondur)
    db.session.add(t)

    # Try to add the target on the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + e.message, 409)

    return utils.response('OK: "' + name + '" -> created', 200)


@app.route("/target/edit", methods=["POST"])
def target_edit():
    """Edit a target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    name = request.form["name"]
    new_name = request.form["new_name"].replace(" ", "")
    new_hostname = request.form["new_hostname"].replace(" ", "")
    new_targettype = request.form["new_targettype"].replace(" ", "")
    new_login = request.form["new_login"].replace(" ", "")
    new_port = request.form["new_port"].replace(" ", "")
    new_sshoptions = request.form["new_sshoptions"]
    new_comment = request.form["new_comment"]
    new_changepwd = request.form["new_changepwd"].replace(" ", "")
    new_sessiondur = ""
    if "new_sessiondur" in request.form:
        # session duration is stored in minutes, but created in hours
        new_sessiondur = int(request.form["new_sessiondur"].replace(" ", ""))*60

    # Check required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    # Check if the name exists in the database
    query = db.session.query(target.Target.name)\
        .filter_by(name=name).first()

    if query is None:
        return utils.response('ERROR: No target with the name "' + name + \
                              '" in the database.', 417)

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
        if name != new_name:
            # Check unicity for name
            query = db.session.query(target.Target.name)\
                .filter_by(name=new_name).first()

            if query is not None and new_name == query.name:
                return utils.response('ERROR: The name "' + new_name + \
                                  '" is already used by another target ', 417)

            to_update.update({"name": new_name})

    if new_targettype:
        if new_targettype not in ["ssh", "mysql", "oracle", "postgresql"]:
            new_targettype = "ssh"
        to_update.update({"targettype": new_targettype})

    if new_changepwd:
        # changepwd is a boolean so we give him the boolean result of this test
        to_update.update({"changepwd": new_changepwd == "True"})

    if new_sessiondur:
        to_update.update({"sessiondur": new_sessiondur})

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + e.message, 409)

    return utils.response('OK: "' + name + '" -> edited', 200)


@app.route("/target/delete/<name>")
def target_delete(name):
    """Delete a target in the database"""
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    # Check if the name exists
    query = db.session.query(target.Target.name)\
        .filter_by(name=name).first()

    if query is None:
        return utils.response('ERROR: No target with the name "' + name + \
                              '" in the database.', 417)

    target_data = target.Target.query.filter_by(name=name).first()
    # Delete the target from the associated targetgroups
    targetgroup_list = target_data.direct_targetgroups()
    for each_targetgroup in targetgroup_list:
        each_targetgroup.rmtarget(target_data)

    # We can now delete the target from the db
    #TODO change the deletion and add deactivate field to True instead
    t = db.session.query(
                 target.Target).filter(
                 target.Target.name == name)
    t[0].prepare_delete()
    t.delete()

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + e.message, 409)

    return utils.response('OK: "' + name + '" -> deleted', 200)


@app.route("/target/adduser", methods=["POST"])
def target_adduser():
    """Add a user in the target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.errormsg("ERROR: POST method is required ", 405)

    # Simplification for the reading
    username = request.form["username"]
    targetname = request.form["targetname"]

    # Check for required fields
    if not username or not targetname:
        return utils.response("ERROR: The username and targetname are" + \
                              " required ", 417)

    # User and target have to exist in database
    u = utils.get_user(username)
    if not u:
        return utils.response('ERROR: no user "' + username + \
                              '" in the database ', 417)

    t = utils.get_target(targetname)
    if not t:
        return utils.response('ERROR: no target "' + targetname + \
                              '" in the database ', 417)

    # Now we can add the user
    t.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + targetname + '" -> ' + \
                               e.message, 409)

    utils.notif("User " + username + " has now access to " + targetname + ".", 
                "[PaSSHport] " + username + " can access " + targetname )
    return utils.response('OK: "' + username + '" added to "' + \
                          targetname + '"', 200)


@app.route("/target/rmuser", methods=["POST"])
def target_rmuser():
    """Remove a user from the target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    username = request.form["username"]
    targetname = request.form["targetname"]

    # Check for required fields
    if not username or not targetname:
        return utils.response("ERROR: The username and targetname are" + \
                              " required ", 417)

    # User and target have to exist in database
    u = utils.get_user(username)
    if not u:
        return utils.response('ERROR: No user "' + username + \
                              '" in the database ', 417)

    t = utils.get_target(targetname)
    if not t:
        return utils.response('ERROR: No target "' + targetname + \
                              '" in the database ', 417)

    # Check if the given user is a member of the given target
    if not t.username_in_target(username):
        return utils.response('ERROR: The user "' + username + \
                              '" is not a member of the target "' + \
                              targetname + '" ', 417)

    # Now we can remove the user
    t.rmuser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + targetname + '" -> ' + \
                              e.message, 409)

    utils.notif("User " + username + " lost access to " + targetname + ".", 
                "[PaSSHport] " + username + " removed from " + targetname )
    return utils.response('OK: "' + username + '" removed from "' + \
                          targetname + '"', 200)


@app.route("/target/addusergroup", methods=["POST"])
def target_addusergroup():
    """Add a usergroup in the target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    targetname = request.form["targetname"]

    # Check for required fields
    if not usergroupname or not targetname:
        return utils.response("ERROR: The usergroupname and targetname are" + \
                              " required ", 417)

    # Usergroup and target have to exist in database
    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return utils.response('ERROR: no usergroup "' + usergroupname + \
                              '" in the database ', 417)

    t = utils.get_target(targetname)
    if not t:
        return utils.response('ERROR: no target "' + targetname + \
                              '" in the database ', 417)

    # Now we can add the user
    t.addusergroup(ug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + targetname + '" -> ' + \
                              e.message, 409)

    utils.notif("Users from group" + usergroupname + " can now access " + \
                targetname + ".\n\nAffected users:\n" + \
                str(ug.all_username_list()), "[PaSSHport] " + usergroupname + \
                " can now access " + targetname)
    return utils.response('OK: "' + usergroupname + '" added to "' + \
                          targetname + '"', 200)


@app.route("/target/rmusergroup", methods=["POST"])
def target_rmusergroup():
    """Remove a usergroup from the target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    usergroupname = request.form["usergroupname"]
    targetname = request.form["targetname"]

    # Check for required fields
    if not usergroupname or not targetname:
        return utils.response("ERROR: The usergroupname and targetname are" + \
                              " required ", 417)

    # Usergroup and target have to exist in database
    ug = utils.get_usergroup(usergroupname)
    if not ug:
        return utils.response('ERROR: No usergroup "' + usergroupname + \
                              '" in the database ', 417)

    t = utils.get_target(targetname)
    if not t:
        return utils.response('ERROR: No target "' + targetname + \
                              '" in the database ', 417)

    # Check if the given usergroup is a member of the given target
    if not t.usergroupname_in_target(usergroupname):
        return utils.response('ERROR: The usergroup "' + usergroupname + \
                              '" is not a member of the target "' + \
                              targetname + '" ', 417)

    # Now we can remove the usergroup
    t.rmusergroup(ug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + targetname + '" -> ' + \
                              e.message, 409)

    utils.notif("Users from group" + usergroupname + " lost access to " + \
                targetname + ".\n\nAffected users:\n" + \
                str(ug.all_username_list()), "[PaSSHport] " + usergroupname + \
                " removed from " + targetname)
    return utils.response('OK: "' + usergroupname + '" removed from "' + \
                          targetname + '"', 200)


@app.route("/target/lastlog/<name>")
def target_lastlog(name):
    """Return the 500 last logs as json"""
    #TODO pagination for ajax call on all logs
    t = utils.get_target(name)
    if not t:
        return "{}"
    return t.get_lastlog()


@app.route("/exttargetaccess/open/<ip>/<targetname>/<username>")
def extgetaccess(ip, targetname, username):
    """Create an external request to open a connection to a target"""

    t = utils.get_target(targetname)
    if not t:
        msg = 'ERROR: No target "' + targetname + '" in the database '
        app.logger.error(msg)
        return utils.response(msg, 417)

    #Date to stop access:
    startdate = datetime.now()
    stopdate  = startdate + timedelta(hours=int(t.show_sessionduration())/60)
    formatedstop = format(stopdate, '%Y%m%dT%H%M')
    
    #Call the external script
    process = Popen([config.OPEN_ACCESS_PATH, 
                    t.show_targettype(),
                    formatedstop,                    
                    ip,
                    t.show_hostname(),
                    str(t.show_port()),
                    username,
                    t.show_name()], stdout=PIPE)

    (output, err) = process.communicate()
    exit_code = process.wait()
    
    if exit_code != 0:
        app.logger.error('External script return ' + str(exit_code))
        app.logger.error('Output message was' + str(output))
        return utils.response('ERROR: external script return ' + \
                               str(exit_code), 500)

    if output:
        # Transform the ouput on Dict
        try:
            output = eval(output)
        except:
            app.logger.error("Error on openaccess return: " + str(output))
            return utils.response('Openaccess script is broken', 400)

        if output["execution_status"] != "OK":
            app.logger.error("Error on openaccess return: " + str(output))
            return utils.response('ERROR: target seems unreachable.',
                                   200)

        # Create a exttarget object to log the connection
        u = utils.get_user(username)
        if not u:
            return utils.response('ERROR: No user "' + username + \
                              '" in the database ', 417)

        ta = exttargetaccess.Exttargetaccess(
            startdate = startdate,
            stopdate = stopdate,
            userip = ip,
            proxy_ip = output["proxy_ip"],
            proxy_pid = output["pid"],
            proxy_port = output["proxy_port"])
        ta.addtarget(t)
        ta.adduser(u)

        db.session.add(ta)

        # Try to add the targetaccess on the database
        try:
            db.session.commit()
        except exc.SQLAlchemyError as e:
            app.logger.error('ERROR registering connection demand: ' + \
                             'exttargetaccess "' + str(output) + '" -> ' +
                             str(e))

        # Create the output to print
        response = "Connect via " + output["proxy_ip"] + " on  port " + \
                   output["proxy_port"] + " until " + \
                   format(stopdate, '%H:%M')
    else:
        return utils.response("Openaccess script is broken", 400)

    app.logger.info(response)
    return utils.response(response, 200)


@app.route("/exttargetaccess/closebyname/<targetname>/<username>")
def extcloseaccessbyname(targetname, username):
    """Close a connection determined by target name and user name"""
    # Determine associated pid
    et = exttargetaccess.Exttargetaccess
    pidlist = et.query.filter(and_(et.target.any(name = targetname), 
                                   et.user.any(name = username),
                                   et.proxy_pid != 0))

    if not pidlist:
        return utils.response("Error: this connection is not registered", 400)
    return extcloseaccess(pidlist[0].proxy_pid, pidlist[0])


@app.route("/exttargetaccess/close/<pid>/<extaccess>")
def extcloseaccess(pid, extaccess):
    """Close a connection determined by the PID"""
    #Call the external script
    process = Popen([config.OPEN_ACCESS_PATH, 
                    "db-close",
                    str(pid)], stdout=PIPE)

    (output, err) = process.communicate()
    exit_code = process.wait()
    
    if exit_code != 0:
        app.logger.error('External script return ' + str(exit_code))
        app.logger.error('Output message was' + str(output))
        return utils.response('ERROR: external script return ' + \
                               str(exit_code), 500)

    if output:
        # Transform the ouput on Dict
        try:
            output = eval(output)
        except:
            app.logger.error("Error on openaccess return: " + str(output))
            return utils.response('Openaccess script is broken', 400)

        if output["execution_status"] != "OK":
            app.logger.error("Error on openaccess return: " + str(output))
            return utils.response('ERROR: connection can not be closed.',
                                   200)

    # Set the exttargetaccess proxy_pid to 0
    extaccess.set_proxy_pid(0)

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR:  impossible to change the pid ' + \
                    'on extarget with pid: "' + pid + '" -> ' + e.message, 409)

    response = "Connection closed. Click to reopen."
    return utils.response(response, 200)


@app.route("/target/getpassword/<targetname>/<number>")
@app.route("/target/getpassword/<targetname>")
def getpassword(targetname, number = 20):
    """Get stored passwords associated to a target, used on automatic 
    root password change by passhport script"""
    
    t = target.Target.query.filter_by(name=targetname).first()
    if t is None:
        return utils.response('ERROR: No target with the name "' + \
                               targetname + '" in the database.', 417)

    # Response for datatable
    output = '[\n'
    i = 1
    tlen = len(t.passentries)
    # We decrypt only 20 first passwords to avoid long waits
    while i < tlen +1 and i < int(number)+1:
        output = output + t.passentries[tlen-i].notargetjson() + ",\n"
        i = i+1

    if output == '[\n':
        return utils.response('[]', 200)
    output = output[:-2] + '\n]'

    return utils.response(output, 200) 
