# -*-coding:Utf-8 -*-

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
        target.Target.targetname).order_by(
        target.Target.targetname).all()

    for row in query:
        result.append(row[0])

    if not result:
        return "No target in database.\n", 200, {"Content-Type": "text/plain"}

    return "\n".join(result), 200, {"Content-Type": "text/plain"}


@app.route("/target/search/<pattern>")
def target_search(pattern):
    """Return a list of targets that match the given pattern"""
    """
    To check
        Specific characters
        upper and lowercases
    """

    result = []
    query  = db.session.query(target.Target.targetname)\
        .filter(target.Target.targetname.like("%" + pattern + "%"))\
        .order_by(target.Target.targetname).all()

    for row in query:
        result.append(row[0])

    if not result:
        return 'No target matching the pattern "' + pattern + \
            '" found.\n', 200, {"Content-Type": "text/plain"}

    return "\n".join(result), 200, {"Content-Type": "text/plain"}


@app.route("/target/show/<targetname>")
def target_show(targetname):
    """Return all data about a user"""
    """
    To check
        Specific characters
        upper and lowercases
    """

    # Check for required fields
    if not targetname:
        return "ERROR: The email is required ", 417, {
            "Content-Type": "text/plain"}

    target_data = target.Target.query.filter_by(targetname=targetname).first()

    if target_data is None:
        return 'ERROR: No target with the name "' + targetname + \
            '" in the database.\n', 417, {"Content-Type": "text/plain"}

    return str(target_data), 200, {"Content-Type": "text/plain"}


@app.route("/target/create", methods=["POST"])
def target_create():
    """Add a target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetname = request.form["targetname"]
    hostname = request.form["hostname"]
    port = request.form["port"]
    sshoptions = request.form["sshoptions"]
    servertype = request.form["servertype"]
    autocommand = request.form["autocommand"]
    comment = request.form["comment"]

    # Check for required fields
    if not targetname or not hostname:
        return "ERROR: The targetname and hostname are required ", 417, {
            "Content-Type": "text/plain"}

    if not port:
        port = 22

    # Check unicity for targetname
    query = db.session.query(target.Target.targetname)\
        .filter_by(targetname=targetname).first()

    if query is not None:
        return 'ERROR: The targetname "' + targetname + \
            '" is already used by another target ',\
             417, {"Content-Type": "text/plain"}

    t = target.Target(
        targetname=targetname,
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
        return 'ERROR: "' + targetname + '" -> ' + e.message + \
            "\n", 409, {"Content-Type": "text/plain"}

    return 'OK: "' + targetname + '" -> created' + \
        "\n", 200, {"Content-Type": "text/plain"}


@app.route("/target/edit", methods=["POST"])
def target_edit():
    """Edit a target in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    targetname = request.form["targetname"]
    new_targetname = request.form["new_targetname"]
    new_hostname = request.form["new_hostname"]
    new_port = request.form["new_port"]
    new_sshoptions = request.form["new_sshoptions"]
    new_servertype = request.form["new_servertype"]
    new_autocommand = request.form["new_autocommand"]
    new_comment = request.form["new_comment"]

    # Check required fields
    if not targetname:
        return "ERROR: The targetname is required ", 417, {
            "Content-Type": "text/plain"}

    # Check if the targetname exists in the database
    query = db.session.query(target.Target)\
        .filter_by(targetname=targetname).first()

    if query is None:
        return 'ERROR: No target with the targetname "' + targetname + \
            '" in the database.\n', 417, {"Content-Type": "text/plain"}

    toupdate = db.session.query(target.Target).filter_by(targetname=targetname)

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
    if new_targetname:
        # Check unicity for targetname
        query = db.session.query(target.Target.targetname)\
            .filter_by(targetname=new_targetname).first()

        if query is not None and new_targetname != query.targetname:
            return 'ERROR: The targetname "' + new_targetname + \
                '" is already used by another target ', \
                417, {"Content-Type": "text/plain"}

        toupdate.update({"targetname": new_targetname})

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetname + '" -> ' + e.message + \
            "\n", 409, {"Content-Type": "text/plain"}

    return 'OK: "' + targetname + '" -> edited' + \
        "\n", 200, {"Content-Type": "text/plain"}


@app.route("/target/delete/<targetname>")
def target_delete(targetname):
    """Delete a target in the database"""
    if not targetname:
        return "ERROR: The targetname is required ", 417, {
            "Content-Type": "text/plain"}

    # Check if the targetname exists
    query = db.session.query(target.Target.targetname)\
        .filter_by(targetname=targetname).first()

    if query is None:
        return 'ERROR: No target with the targetname "' + targetname + \
            '" in the database.\n', 417, {"Content-Type": "text/plain"}

    db.session.query(
        target.Target).filter(
        target.Target.targetname == targetname).delete()

    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return 'ERROR: "' + targetname + '" -> ' + e.message + \
            "\n", 409, {"Content-Type": "text/plain"}

    return 'OK: "' + targetname + '" -> deleted' + \
        "\n", 200, {"Content-Type": "text/plain"}


@app.route('/target/adduser', methods=['POST'])
def target_adduser():
    """Add a user in the target in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {
            'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetname = request.form['targetname']
    email = request.form['email']

    # Check for mandatory fields
    if not targetname or not email:
        return "ERROR: The targetname and email are required ", 417, {
            'Content-Type': 'text/plain'}

    # Target and user have to exist in database
    t = get_target(targetname)
    if not t:
        return 'ERROR: no target "' + targetname + \
            '" in the database ', 417, {'Content-Type': 'text/plain'}

    u = get_user(email)
    if not u:
        return 'ERROR: no user "' + email + \
            '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Now we can add the user
    t.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetname + '" -> ' + e.message + \
            '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + email + '" added to "' + targetname + \
        '"', 200, {'Content-Type': 'text/plain'}


@app.route('/target/rmuser', methods=['POST'])
def target_rmuser():
    """Remove a user from the target in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {
            'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetname = request.form['targetname']
    email = request.form['email']

    # Check for mandatory fields
    if not targetname or not email:
        return "ERROR: The targetname and email are required ", 417, {
            'Content-Type': 'text/plain'}

    # Target and user have to exist in database
    t = get_target(targetname)
    if not t:
        return 'ERROR: No target "' + targetname + \
            '" in the database ', 417, {'Content-Type': 'text/plain'}

    u = get_user(email)
    if not u:
        return 'ERROR: No user "' + email + \
            '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Check if the given user is a member of the given target
    if not t.email_in_target(email):
        return 'ERROR: The user "' + email + '" is not a member of the target "' + \
            targetname + '" ', 417, {'Content-Type': 'text/plain'}

    # Now we can remove the user
    t.rmuser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetname + '" -> ' + e.message + \
            '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + email + '" removed from "' + \
        targetname + '"', 200, {'Content-Type': 'text/plain'}


@app.route('/target/addusergroup', methods=['POST'])
def target_addusergroup():
    """Add a usergroup in the target in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {
            'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetname = request.form['targetname']
    usergroupname = request.form['usergroupname']

    # Check for mandatory fields
    if not targetname or not usergroupname:
        return "ERROR: The targetname and usergroupname are required ", 417, {
            'Content-Type': 'text/plain'}

    # Target and user have to exist in database
    t = get_target(targetname)
    if not t:
        return 'ERROR: no target "' + targetname + \
            '" in the database ', 417, {'Content-Type': 'text/plain'}

    g = get_usergroup(usergroupname)
    if not g:
        return 'ERROR: no usergroup "' + usergroupname + \
            '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Now we can add the user
    t.addusergroup(g)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetname + '" -> ' + e.message + \
            '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + usergroupname + '" added to "' + \
        targetname + '"', 200, {'Content-Type': 'text/plain'}


@app.route('/target/rmusergroup', methods=['POST'])
def target_rmusergroup():
    """Remove a usergroup from the target in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {
            'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetname = request.form['targetname']
    usergroupname = request.form['usergroupname']

    # Check for mandatory fields
    if not targetname or not usergroupname:
        return "ERROR: The targetname and usergroupname are required ", 417, {
            'Content-Type': 'text/plain'}

    # Target and user have to exist in database
    t = get_target(targetname)
    if not t:
        return 'ERROR: No target "' + targetname + \
            '" in the database ', 417, {'Content-Type': 'text/plain'}

    u = get_usergroup(usergroupname)
    if not u:
        return 'ERROR: No usergroup "' + usergroupname + \
            '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Check if the given usergroup is a member of the given target
    if not t.usergroupname_in_target(usergroupname):
        return 'ERROR: The usergroup "' + usergroupname + '" is not a member of the target "' + \
            targetname + '" ', 417, {'Content-Type': 'text/plain'}

    # Now we can remove the usergroup
    t.rmusergroup(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + targetname + '" -> ' + e.message + \
            '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + usergroupname + '" removed from "' + \
        targetname + '"', 200, {'Content-Type': 'text/plain'}

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


def get_user(email):
    """Return the user with the given email"""
    u = db.session.query(user.User).filter(
        user.User.email == email).all()

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
