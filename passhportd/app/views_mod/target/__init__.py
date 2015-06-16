# -*-coding:Utf-8 -*-

from app import app
from flask          import request
from sqlalchemy     import exc
from sqlalchemy.orm import sessionmaker
from app            import app, db
from app.models_mod import target
from app.models_mod import user
from app.models_mod import usergroup

@app.route("/target/list")
def target_list():
    """Return the target list of database"""
    result = []
    query  = db.session.query(target.Target.targetname).order_by(target.Target.targetname)

    for row in query.all():
        result.append(str(row[0]).encode('utf8'))

    if not result:
        return "No target in database.\n", 200, {'Content-Type': 'text/plain'}

    return '\n'.join(result), 200, {'Content-Type': 'text/plain'}

@app.route('/target/search/<pattern>')
def target_search(pattern):
    """Return a list of targets that match the given pattern"""
    """
    To check
        pattern not in db
        Specific characters
        upper and lowercases
    """

    result = []
    query  = db.session.query(target.Target.targetname)\
            .filter(target.Target.targetname.like('%' + pattern + '%'))

    for row in query.all():
        result.append(str(row[0]).encode('utf8'))

    if not result:
        return 'No target matching the pattern "' + pattern + '" found.\n', 200, {'Content-Type': 'text/plain'}

    return '\n'.join(result), 200, {'Content-Type': 'text/plain'}

@app.route('/target/show/<targetname>')
def target_show(targetname):
    """Return all data about a user"""
    """
    To check
        pattern not in db
        Specific characters
        upper and lowercases
    """

    target_data = target.Target.query.filter_by(targetname = targetname).first()

    if target_data is None:
        return 'ERROR: No target with the name "' + targetname + '" in the database.\n', 417, {'Content-Type': 'text/plain'}

    return str(target_data), 200, {'Content-Type': 'text/plain'}

@app.route('/target/create', methods = ['POST'])
def target_create():
    """Add a target in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetname  = request.form['targetname']
    hostname    = request.form['hostname']
    port        = request.form['port']
    sshoptions  = request.form['sshoptions']
    servertype  = request.form['servertype']
    autocommand = request.form['autocommand']
    comment     = request.form['comment']

    # Check for mandatory fields
    if not targetname or not hostname:
        return "ERROR: The targetname and hostname are required ", 417, {'Content-Type': 'text/plain'}

    if not port:
        port = "22"

    # Check unicity for targetname
    query = db.session.query(target.Target.targetname)\
        .filter(target.Target.targetname.like(targetname))

    # normally only one row
    for row in query.all():
        if str(row[0]) == targetname:
            return 'ERROR: The targetname "' + targetname + '" is already used by another target ', 417, {'Content-Type': 'text/plain'}

    t = target.Target(
            targetname  = targetname,
            hostname    = hostname,
            port        = port,
            sshoptions  = sshoptions,
            servertype  = servertype,
            autocommand = autocommand,
            comment     = comment)
    db.session.add(t)

    # Try to add the target on the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + targetname + '" -> created' + '\n', 200, {'Content-Type': 'text/plain'}

@app.route('/target/edit/', methods = ['POST'])
def target_edit():
    """Edit a target in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetname          = request.form['targetname']
    new_targetname      = request.form['new_targetname']
    new_hostname        = request.form['new_hostname']
    new_port            = request.form['new_port']
    new_sshoptions      = request.form['new_sshoptions']
    new_servertype      = request.form['new_servertype']
    new_autocommand     = request.form['new_autocommand']
    new_comment         = request.form['new_comment']

    toupdate = db.session.query(target.Target).filter_by(targetname = targetname)

    # Let’s modify only relevent fields
    if new_sshoptions:
        toupdate.update({'sshoptions': str(new_sshoptions).encode('utf8')})
    if new_servertype:
        toupdate.update({'servertype': str(new_servertype).encode('utf8')})
    if new_autocommand:
        toupdate.update({'autocommand': str(new_autocommand).encode('utf8')})
    if new_comment:
        toupdate.update({'comment': str(new_comment).encode('utf8')})
    if new_port:
        toupdate.update({'port': new_port})
    if new_hostname:
        toupdate.update({'hostname': str(new_hostname).encode('utf8')})
    if new_targetname:
        toupdate.update({'targetname': str(new_targetname).encode('utf8')})

    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + targetname + '" -> edited' + '\n', 200, {'Content-Type': 'text/plain'}

@app.route('/target/del/<targetname>')
def target_del(targetname):
    """Delete a target in the database"""
    if not targetname:
        return "ERROR: The targetname is required ", 417, {'Content-Type': 'text/plain'}

    # Check if the targetname exists
    query = db.session.query(target.Target.targetname)\
            .filter(target.Target.targetname.like(targetname))

    # Normally only one row
    for row in query.all():
        if str(row[0]) == targetname:
            db.session.query(target.Target).filter(target.Target.targetname == targetname).delete()

            try:
                db.session.commit()
            except exc.SQLAlchemyError:
                return 'ERROR: "' + targetname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

            return 'OK: "' + targetname + '" -> deleted' + '\n', 200, {'Content-Type': 'text/plain'}

    return 'ERROR: No target with the targetname "' + targetname + '" in the database.\n', 417, {'Content-Type': 'text/plain'}

@app.route('/target/adduser', methods = ['POST'])
def target_adduser():
    """Add a user in the target in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetname  = request.form['targetname']
    email       = request.form['email']

    # Check for mandatory fields
    if not targetname or not email:
        return "ERROR: The targetname and email are required ", 417, {'Content-Type': 'text/plain'}

    # Target and user have to exist in database
    t = get_target(targetname)
    if not t:
        return 'ERROR: no target "' + targetname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    u = get_user(email)
    if not u:
        return 'ERROR: no user "' + email + '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Now we can add the user
    t.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return '"' + email + '" added to "' + targetname + '"', 200, {'Content-Type': 'text/plain'}

@app.route('/target/rmuser', methods = ['POST'])
def target_rmuser():
    """Remove a user from the target in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetname = request.form['targetname']
    email      = request.form['email']

    # Check for mandatory fields
    if not targetname or not email:
        return "ERROR: The targetname and email are required ", 417, {'Content-Type': 'text/plain'}

    # Target and user have to exist in database
    t = get_target(targetname)
    if not t:
        return 'ERROR: no target "' + targetname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    u = get_user(email)
    if not u:
        return 'ERROR: no user "' + email + '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Now we can remove the user
    t.rmuser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return '"' + email + '" removed from "' + targetname + '"', 200, {'Content-Type': 'text/plain'}


@app.route('/target/addusergroup/',methods=['POST'])
def target_addusergroup():
    " Has to be tested "
    # Only POST data are handled
    if request.method != 'POST':
        return "POST Method is mandatory\n"

    # Simplification for the reading
    targetname      = request.form['targetname']
    usergroupname   = request.form['usergroupname']

    if len(targetname) <= 0 or len(usergroupname) <= 0 :
        return "ERROR: targetname and usergroupname are mandatory\n"

    # Target and user have to exist in database
    t = get_target(targetname)
    if t == False:
        return "Error: target does not exist\n"

    g = get_ugroup(usergroupname)
    if g == False:
        return "Error: usergroup does not exist\n"

    # Now we can add the user
    t.addusergroup(g)
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return "ERROR: " + exc

    return usergroupname + " added to " + targetname + "\n"


@app.route('/target/rmusergroup/',methods=['POST'])
def target_rmusergroup():
    """ Has to be tested """
    # Only POST data are handled
    if request.method != 'POST':
        return "POST Method is mandatory\n"

    # Simplification for the reading
    targetname      = request.form['targetname']
    usergroupname   = request.form['usergroupname']

    if len(targetname) <= 0 or len(usergroupname) <= 0 :
        return "ERROR: targetname and usergroupname are mandatory\n"

    # Target and user have to exist in database
    t = get_target(targetname)
    if t == False:
        return "Error: target does not exist\n"

    g = get_ugroup(usergroupname)
    if g == False:
        return "Error: usergroup does not exist\n"

    # Now we can add the user
    t.rmusergroup(g)
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return "ERROR: " + exc

    return usergroupname + " added to " + targetname + "\n"



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
