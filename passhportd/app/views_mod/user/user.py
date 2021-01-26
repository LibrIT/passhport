# -*- coding:Utf-8 -*-


import os, sys, stat, re
import config

from io import open
from ldap3 import Server, Connection, ALL
from ldap3.utils.dn import escape_rdn
from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import user, target
from . import api
from .. import utilities as utils


def useruid(s, login):
    """Connect to a LDAP and check the uid matching the given field data"""
    uid = False
    c = Connection(s, config.LDAPACC, 
                   password=config.LDAPPASS, auto_bind=True)

    if c.result["description"] != "success":
        app.logger.error("Error connecting to the LDAP with the service account")
        return False

    # Look for the user entry.
    if not c.search(config.LDAPBASE,
                    "(" + config.LDAPFIELD + "=" + login + ")") :
        app.logger.error("Error: Connection to the LDAP with service account failed")
    else:
        if len(c.entries) >= 1 :
            if len(c.entries) > 1 :
                app.logger.error("Error: multiple entries with this login. "+ \
                          "Trying first entry...")
            uid = c.entries[0].entry_dn
        else:
            app.logger.error("Error: Login not found")
        c.unbind()
    
    return uid


def try_ldap_login(login, password):
    """ Connect to a LDAP directory to verify user login/passwords"""
    result = "Wrong login/password"
    s = Server(config.LDAPURI, port=config.LDAPPORT,
               use_ssl=False, get_info=ALL)
    # 1. connection with service account to find the user uid
    uid = useruid(s, login)
   
    if uid: 
        # 2. Try to bind the user to the LDAP
        c = Connection(s, user = uid , password = password, auto_bind = True)
        c.open()
        c.bind()
        result =  c.result["description"] # "success" if bind is ok
        c.unbind()

    return result


def try_login(login, password, method="LDAP"):
    if method == "LDAP":
        return try_ldap_login(login, password)


@app.route("/user/login", methods=["POST"])
def user_login():
    """Allow passhportd to handle login/passwords for users"""
    # Only POST data are handled
    if request.method != "POST":
        return utils.response("ERROR: POST method is required ", 405)

    # Simplification for the reading
    login = request.form["login"]
    password = request.form["password"]

    # Check for required fields
    if not login or not password:
        return utils.response("ERROR: The login and password are required ", 417)
    elif login != escape_rdn(login):
        return utils.response("ERROR: Bad input", 417)

    # Check data validity uppon LDAP/local/whatever...
    result = try_login(login, password)
    if result == "success":
        app.logger.info("Authentication ok for {}".format(login))
        # If the LDAP connection is ok, user can connect
        return utils.response("Authorized", 200)
    app.logger.warning("Authentication error for {} => ".format(login) + str(result))
    return utils.response("Refused: " + str(result), 200)


@app.route("/user/list")
def user_list():
    """Return the user list of database"""
    result = []
    query = db.session.query(user.User.name).order_by(user.User.name).all()

    for row in query:
        result.append(row[0])

    if not result:
        return utils.response("No user in database.", 200)

    return utils.response("\n".join(result), 200)


@app.route("/user/search/<pattern>")
def user_search(pattern):
    """Return a list of users that match the given pattern"""
    result = []
    query  = db.session.query(user.User.name)\
        .filter(user.User.name.like("%" + pattern + "%"))\
        .order_by(user.User.name).all()

    for row in query:
        result.append(row[0])

    if not result:
        return utils.response('No user matching the pattern "' + pattern + \
                              '" found.', 200)

    return utils.response("\n".join(result), 200)


@app.route("/user/show/<name>")
def user_show(name):
    """Return all data about a user"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    user_data = user.User.query.filter_by(name=name).first()

    if user_data is None:
        return utils.response('ERROR: No user with the name "' + name + \
                              '" in the database.', 417)

    return utils.response(user_data.__repr__(), 200)

@app.route("/user/access/<name>")
def user_access(name):
    """Return all the targets accessible for this user in a simple way"""
    if not name:
    	return utils.response("ERROR: The name is required ", 417)

    user_data = user.User.query.filter_by(name=name).first()

    if user_data is None:
        return utils.response('ERROR: No user with the name "' + name + \
                              '" in the database.', 417)

    return utils.response(str(user_data.accessible_target_list("names")), 200)


@app.route("/user/memberof/<obj>/<name>")
def user_memberof(obj, name):
    """Return the list of obj this user is member of"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    user_data = user.User.query.filter_by(name=name).first()

    if user_data is None:
        return utils.response('ERROR: No user with the name "' + name + \
                              '" in the database.', 417)

    return utils.response(str(user_data.memberof(obj)), 200)


def atoi(text):
    return int(text) if text.isdigit() else text


def naturalkeys(text):
    """ stackoverflow how-to-correctly-sort-a-string-with-a-number-inside
        and http://nedbatchelder.com/blog/200712/human_sorting.html 
        basically sort a text list taking care of numbers """
    return [ atoi(c) for c in re.split('(\d+)', text) ]


def uaccessible_targets(name, withid = True, returnlist = False):
    """Return the list of the targets that the user can access
       with the ID or without the ID of the target"""
    # Check for required fields
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    user_data = user.User.query.filter_by(name=name).first()

    if user_data is None:
        return utils.response('ERROR: No user with the name "' + name + \
                              '" in the database.', 417)

    target_list = user_data.accessible_target_list()
    formatted_target_list = []

    for each_target in target_list:
        # We show only ssh targets, other types will not be handle here
        if each_target.show_targettype() == "ssh":
            data = ""
            if withid:
                data = str(each_target.id) + " "
            data = data + each_target.show_name() + " " + \
                   each_target.show_hostname() + " " + \
                   each_target.show_comment()
            formatted_target_list.append(data)
    if returnlist:
        return [target.show_name() for target in target_list 
                if target.show_targettype() == "ssh"]
    if withid:
        # We need to be sorted by target ID. Not so easy cause ID are strings
        formatted_target_list.sort(key=naturalkeys) #naturalkey is a method right above
    return utils.response("\n".join(formatted_target_list), 200)


@app.route("/user/accessible_targets/<name>")
def user_accessible_targets(name, returnlist = False):
    """Return the list of targets that the user can access"""
    return  uaccessible_targets(name, False, returnlist)


@app.route("/user/accessible_idtargets/<name>")
def user_accessible_idtargets(name, returnlist = False):
    """Return the list of targets that the user can access with ID"""
    return  uaccessible_targets(name, True, returnlist)


@app.route("/user/accessible_target/<username>/<targetname>")
def user_accssible_target(username, targetname):
    """ Return True if the user can access this target, else return False """
    # Check for required fields
    if not username or not targetname:
        return utils.response("ERROR: Username or targetname is missing ", 417)
    
    if targetname in user_accessible_targets(username, returnlist = True):
        return utils.response("True", 200)
    return utils.response("False", 200)


def check_user_form(mandatory, request):
    """Check the user form to test several mandatory elements"""
    # Must be POST
    if not utils.is_post(request):
        return utils.response("ERROR: POST method is required ", 405)

    form = request.form
    # Check mandatory fields
    if utils.miss_mandatory(mandatory, form):
        return utils.response("ERROR: The name and SSH key are required ", 417)

    # User can't have same username
    if utils.name_already_taken(form["name"]):
        return utils.response("ERROR: The name is already taken ", 417)
    # User name can't contain spaces
    if form["name"] != form["name"].replace(" ",""):
        return utils.response("ERROR: The name can't contain spaces.", 417)
    
    # Check SSHkey format
    hashkey = utils.sshkey_good_format(form["sshkey"])
    if not hashkey:
        return utils.response("ERROR: The SSHkey format is not recognized", 417)

    # Check SSHkey unicity
    if utils.sshkey_already_taken(hashkey):
        return utils.response("ERROR: Another user is using this SSHkey ", 417)

    return True


@app.route("/user/create", methods=["POST"])
def user_create():
    """Add a user in the database"""
    # Check if fields are OK to be imported
    # Some fields are mandatory
    res = check_user_form(["name", "sshkey"],
                          request)
    if res is not True:
        return res

    hashkey = utils.sshkey_good_format(request.form["sshkey"])

    if request.form.get("logfilesize"):
        u = user.User(
            name=request.form["name"],
            sshkey=request.form["sshkey"],
            sshkeyhash= utils.sshkey_good_format(request.form["sshkey"]),
            comment=request.form["comment"],
            logfilesize=request.form.get("logfilesize"))
    else:
        u = user.User(
            name=request.form["name"],
            sshkey=request.form["sshkey"],
            sshkeyhash=hashkey,
            comment=request.form["comment"])

    res = utils.db_add_commit(u)
    if res is not True:
        return res

    # Add the SSH key in the file authorized_keys
    res = utils.write_authorized_keys(request.form["name"], 
                                      request.form["sshkey"])
    if res is not True:
        return res

    return utils.response('OK: "' + request.form["name"] + '" -> created', 200)


@app.route("/user/togglesuperadmin/<name>", methods=["GET"])
def user_togglesuperadmin(name):
    """Change superadmin status of this user"""
    userobj = utils.check_user_get(request, name)
    if not userobj:
        return utils.response("ERROR: The request is not correct. " + \
                "Are you sure this user is register on passhport?", 417)

    # Toggle the superadmin flag
    new_state = userobj.togglesuperadmin()

    res = utils.db_commit()
    if res is not True:
        return res

    return utils.response(new_state, 200)


@app.route("/user/issuperadmin/<name>", methods=["GET"])
def user_issuperadmin(name):
    """Return True if the user is superadmin"""
    userobj = utils.check_user_get(request, name)
    if not userobj:
        return utils.response("ERROR: The request is not correct. " + \
                "Are you sure this user is register on passhport?", 417)

    return utils.response(str(userobj.superadmin), 200)
    

@app.route("/user/generate_authorized_keys", methods=["GET"])
@app.route("/user/generate/authorized_keys", methods=["GET"])
def generate_authorized_keys():
    """Return a authorized_key files with all users"""
    query = db.session.query(user.User).order_by(user.User.name).all()
    r = ""
    
    for userdata in query:
        r = r + 'command="' + config.PYTHON_PATH + " " + \
                config.PASSHPORT_PATH + " " + userdata.name + \
                '" ' + userdata.sshkey + "\n"
    return r


def update_authorized_keys(orig_name, orig_sshkey, new_name, new_sshkey):
    """Edit the ssh autorized_keys file"""
    
    warning = "OK"
    
    # Set empty fields
    if not new_name:
        new_name = orig_name
    if not new_sshkey:
        new_sshkey = orig_sshkey

    # Line supposed to be in the authorized_file
    authorized_keys_line = 'command="' + config.PYTHON_PATH + \
                           " " + config.PASSHPORT_PATH + \
                           " " + orig_name + '" ' + orig_sshkey + "\n"

    # Edit the SSH key in the file authorized_keys
    try:
        with open(config.SSH_KEY_FILE, "r+", encoding="utf8") as \
                  authorized_keys_file:
            line_edited = False
            content = authorized_keys_file.read()
            authorized_keys_file.seek(0)

            for line in content.split('\n')[:-1]:
                if not line_edited:
                    if line != authorized_keys_line[:-1]:
                        authorized_keys_file.write(line + '\n')
                    else:
                        authorized_keys_file.write(
                                'command="' + config.PYTHON_PATH + \
                                " " + config.PASSHPORT_PATH + \
                                " " + new_name + '" ' + new_sshkey + "\n")
                        line_edited = True
                else:
                    if line == authorized_keys_line[:-1]:
                        warning = ("WARNING: There is more " + \
                                   "than one line with this name and sshkey " + \
                                   orig_name + " - " + orig_sshkey + \
                                   ", probably added manually. " + \
                                   "You should edit it manually")

                    authorized_keys_file.write(line + '\n')

            authorized_keys_file.truncate()

    except IOError:
        warning = utils.response('ERROR: cannot write in the file "' + \
                                 '"authorized_keys"', 500)

    return warning


def check_user_editform(mandatory, request):
    """Check the user form to test several mandatory elements"""
    # Must be POST
    if not utils.is_post(request):
        return utils.response("ERROR: POST method is required.", 405)

    form = request.form
    # Check mandatory fields
    if utils.miss_mandatory(mandatory, form):
        return utils.response("ERROR: The name is required.", 417)

    # User must exit in database
    if not utils.name_already_taken(form["name"]):
        return utils.response("ERROR: User doesn't exist.", 417)

    if form["new_name"]:
        # User can't have same username
        if form["new_name"] != form["new_name"].replace(" ",""):
            return utils.response("ERROR: The name can't contain spaces.", 417)
        if form["new_name"] != form["name"] and  utils.name_already_taken(form["new_name"]):
            return utils.response("ERROR: The name is already taken.", 417)
    
    if form["new_sshkey"]:
        # Check SSHkey format
        hashkey = utils.sshkey_good_format(form["new_sshkey"])
        if not hashkey:
            return utils.response(
                             "ERROR: The SSHkey format is not recognized.", 417)

        # Check SSHkey unicity
        userwiththiskey = utils.get_key(hashkey)
        if userwiththiskey:
            if userwiththiskey.name != form["name"]:
                return utils.response(
                              "ERROR: Another user is using this SSHkey.", 417)

    return True


@app.route("/user/edit", methods=["POST"])
def user_edit():
    """Edit a user in the database"""
    # Check if fields are OK to be imported
    res = check_user_editform(["name"], request)
    if res is not True:
        return res

    need_authorizedkey_update = False
    form = request.form
    usertoupdate = db.session.query(user.User.name).filter_by(
                                                     name=form["name"])
    legacysshkey = db.session.query(user.User.sshkey).filter_by(
                                            name=form["name"]).first()[0]

    # Comment
    if form["new_comment"]:
        # This specific string allows admins to remove old comments of the user
        if form["new_comment"] == "PASSHPORTREMOVECOMMENT":
            form["new_comment"] = ""
        usertoupdate.update({"comment": form["new_comment"]})

    # SSHkey / Hash
    if form["new_sshkey"]:
        usertoupdate.update({"sshkey": form["new_sshkey"]})
        usertoupdate.update({"sshkeyhash": user.User.hash(form["new_sshkey"])})
        need_authorizedkey_update = True

    # Username
    if form["new_name"]:
        usertoupdate.update({"name": form["new_name"]})
        need_authorizedkey_update = True

    # Logfilesize
    if form.get("new_logfilesize"):
        usertoupdate.update({"logfilesize": form["new_logfilesize"]})


    # Edit authorized_keys to change username or sshkey or both
    if need_authorizedkey_update:
        res = update_authorized_keys(form["name"], legacysshkey, \
                              form["new_name"], form["new_sshkey"])
        if res != "OK":
            return res

    res = utils.db_commit()
    if res is not True:
        return res

    return utils.response('OK: "' + form["name"] + '" -> edited', 200)


@app.route("/user/delete/<name>")
def user_delete(name):
    """Delete a user in the database
       in the authorizedkey file
       in the associated targets
       and in the associated groups"""
    if not name:
        return utils.response("ERROR: The name is required ", 417)

    # Check if the name exists
    query = db.session.query(user.User).filter_by(name=name).first()

    if query is None:
        return utils.response('ERROR: No user with the name "' + name + \
                              '" in the database.', 417)
            
    authorized_key_line = 'command="' + config.PYTHON_PATH + \
                          " " + config.PASSHPORT_PATH + \
                          " " + name + '" ' + query.sshkey + "\n"

    # Delete the SSH key from the file authorized_keys
    warning = ""
    try:
        with open(config.SSH_KEY_FILE, "r+", encoding="utf8") as \
            authorized_keys_file:
            line_deleted = False
            content = authorized_keys_file.read()
            authorized_keys_file.seek(0)

            for line in content.split('\n')[:-1]:
                if not line_deleted:
                    if line != authorized_key_line[:-1]:
                        authorized_keys_file.write(line + '\n')
                    else:
                        line_deleted = True
                else:
                    if line == authorized_key_line[:-1]:
                        warning = ("\nWARNING: There is more than one line "
                            "with the sshkey " + query.sshkey + ", probably "
                            "added manually. You should delete it manually")

                    authorized_keys_file.write(line + '\n')

            authorized_keys_file.truncate()
    except IOError:
        return utils.response('ERROR: cannot write in the file ' + \
                              '"authorized_keys"', 500)

    # Delete the user from the associated targets
    user_data = user.User.query.filter_by(name=name).first()
 
    target_list = user_data.direct_targets()
    for each_target in target_list:
        each_target.rmuser(user_data)

    # Delete the user form the associated usergroups
    usergroup_list = user_data.direct_usergroups()
    for each_usergroup in usergroup_list:
        each_usergroup.rmuser(user_data)

    # Delete the user form the associated targetgroups
    targetgroup_list = user_data.direct_targetgroups()
    for each_targetgroup in targetgroup_list:
        each_targetgroup.rmuser(user_data)

    # Delete the log entries
    for lentry in user_data.logentries:
        lentry.user.remove(lentry.user[0])
	
    # Finally delet the user from the db
    db.session.query(
        user.User).filter(
        user.User.name == name).delete()

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + e.message, 409)

    return utils.response('OK: "' + name + '" -> deleted' + warning, 200)


@app.route("/user/lastlog/<name>")
def user_lastlog(name):
    """Return the 500 last logs as json"""
    u = utils.get_user(name)
    if not u:
        return "{}"
    return u.get_lastlog()


@app.route("/user/ismanager/<name>", methods=["GET"])
def user_is_manager(name):
    """Return True if the user is a manager of any usergroup"""
    u = utils.check_user_get(request, name)
    if not u:
        return utils.response("ERROR: The request is not correct", 417)

    return utils.response(str(u.is_manager()), 200)


@app.route("/user/generate/sshkeyhash", methods=["GET"])
def generate_sshkeyhash():
    """Re generate the sshkey hash for all users"""
    query = db.session.query(user.User).order_by(user.User.name).all()
    
    for u in query:
        u.sshkeyhash=u.hash(u.sshkey)

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + e.message, 409)

    return utils.response('OK: All sshkey hash generated', 200)

   
@app.route("/user/attachedto/usergroup/<name>")
def user_attached_to_usergroup(name):
    """Return the list of the usergroups that contains this user"""
    u = utils.check_user_get(request, name)
    if not u:
        return utils.response("ERROR: The request is not correct", 417)

    return utils.response(str(u.show_usergroup()), 200)
    
