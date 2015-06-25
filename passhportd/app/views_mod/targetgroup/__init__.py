# -*-coding:Utf-8 -*-

from app            import app, db
from flask          import request
from app.models_mod import targetgroup
from app.models_mod import target
from app.models_mod import user
from app.models_mod import usergroup

@app.route("/targetgroup/list")
def targetgroup_list():
    """Return the targetgroup list of database"""
    result = []
    query  = db.session.query(targetgroup.Targetgroup.targetgroupname).order_by(targetgroup.Targetgroup.targetgroupname)

    for row in query.all():
        result.append(str(row[0].encode('utf8')))

    if not result:
        return "No targetgroup in database.\n", 200, {'Content-Type': 'text/plain'}

    return "\n".join(result), 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/search/<pattern>')
def targetgroup_search(pattern):
    """Return a list of targetgroups that match the given pattern"""
    result = []
    query  = db.session.query(targetgroup.Targetgroup.targetgroupname)\
            .filter(targetgroup.Targetgroup.targetgroupname.like('%' + pattern + '%'))

    for row in query.all():
        result.append(str(row[0]).encode('utf8'))

    if not result:
        return 'No targetgroup matching the pattern "' + pattern + '" found.\n', 200, {'Content-Type': 'text/plain'}

    return '\n'.join(result), 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/show/<targetgroupname>')
def targetgroup_show(targetgroupname):
    """Return all data about a targetgroup"""
    targetgroup_data = targetgroup.Targetgroup.query.filter_by(targetgroupname = targetgroupname).first()

    if targetgroup_data is None:
        return 'ERROR: No targetgroup with the name "' + targetgroupname + '" in the database.\n', 417, {'Content-Type': 'text/plain'}

    return str(targetgroup_data), 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/create', methods = ['POST'])
def targetgroup_create():
    """Add a targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetgroupname = request.form['targetgroupname']
    comment         = request.form['comment']

    # Check for mandatory fields
    if not targetgroupname:
        return "ERROR: The targetgruopname is required ", 417, {'Content-Type': 'text/plain'}

    # Check unicity for targetgroupname
    query = db.session.query(targetgroup.Targetgroup.targetgroupname)\
        .filter(targetgroup.Targetgroup.targetgroupname.like(targetgroupname))

    # Normally only one row
    for row in query.all():
        if str(row[0]) == targetgroupname:
            return 'ERROR: The targetgroupname "' + targetgroupname + '" is already used by another targetgroup ', 417, {'Content-Type': 'text/plain'}

    t = targetgroup.Targetgroup(
            targetgroupname    = targetgroupname,
            comment            = comment)
    db.session.add(t)

    # Try to add the targetgroup in the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetgroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + targetgroupname + '" -> created' + '\n', 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/edit', methods = ['POST'])
def targetgroup_edit():
    """Edit a targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetgroupname     = request.form['targetgroupname']
    new_targetgroupname = request.form['new_targetgroupname']
    new_comment         = request.form['new_comment']

    toupdate = db.session.query(targetgroup.Targetgroup).filter_by(targetgroupname = targetgroupname)

    # Let's modify only relevent fields
    if new_comment:
        toupdate.update({'comment': str(new_comment).encode('utf8')})
    if new_targetgroupname:
        toupdate.update({'targetgroupname': str(new_targetgroupname).encode('utf8')})

    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetgroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + targetgroupname + '" -> edited' + '\n', 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/del/<targetgroupname>')
def targetgroup_del(targetgroupname):
    """Delete a targetgroup in the database"""
    if not targetgroupname:
        return "ERROR: The targetgroupname is required ", 417, {'Content-Type': 'text/plain'}

    # Check if the targetname exists
    query = db.session.query(targetgroup.Targetgroup.targetgroupname)\
            .filter(targetgroup.Targetgroup.targetgroupname.like(targetgroupname))

    # Normally only one row
    for row in query.all():
        if str(row[0]) == targetgroupname:
            db.session.query(targetgroup.Targetgroup).filter(targetgroup.Targetgroup.targetgroupname == targetgroupname).delete()

            try:
                db.session.commit()
            except exc.SQLAlchemyError:
                return 'ERROR: "' + targetgroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

            return 'OK: "' + targetgroupname + '" -> deleted' + '\n', 200, {'Content-Type': 'text/plain'}

    return 'ERROR: No targetgroup with the name "' + targetgroupname + '" in the database.\n', 417, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/addtarget', methods = ['POST'])
def targetgroup_addtarget():
    """Add a target in the targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetname      = request.form['targetname']
    targetgroupname = request.form['targetgroupname']

    # Check for mandatory fields
    if not targetname or not targetgroupname:
        return "ERROR: The targetname and targetgroupname are required ", 417, {'Content-Type': 'text/plain'}

    # Targetgroup and target have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    t = get_target(targetname)
    if not t:
        return 'ERROR: no target "' + targetname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Now we can add the target
    tg.addtarget(t)
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetgroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + targetname + '" added to "' + targetgroupname + '"', 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/rmtarget', methods = ['POST'])
def targetgroup_rmtarget():
    """Remove a target from the targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetname      = request.form['targetname']
    targetgroupname = request.form['targetgroupname']

    # Check for required fields
    if not targetname or not targetgroupname:
        return "ERROR: The targetname and targetgroupname are required ", 417, {'Content-Type': 'text/plain'}

    # Targetgroup and target have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: No targetgroup "' + targetgroupname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    t = get_target(targetname)
    if not t:
        return 'ERROR: No target "' + targetname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Check if the given target is a member of the given targetgroup
    if not tg.name_in_targetgroup(targetname):
        return 'ERROR: The target "' + target + '" is not a member of the targetgroup "' + targetgroupname + '" ', 417, {'Content-Type': 'text/plain'}

    # Now we can remove the target
    tg.rmtarget(t)
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetgroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + targetname + '" removed from "' + targetgroupname + '"', 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/adduser', methods = ['POST'])
def targetgroup_adduser():
    """Add a user in the targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetgroupname = request.form['targetgroupname']
    email           = request.form['email']

    # Check for required fields
    if not targetgroupname or not email:
        return "ERROR: The targetgroupname and email are required ", 417, {'Content-Type': 'text/plain'}

    # Targetgroup and user have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    u = get_user(email)
    if not u:
        return 'ERROR: no user "' + email + '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Now we can add the user
    tg.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetgroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + email + '" added to "' + targetgroupname + '"', 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/rmuser', methods = ['POST'])
def targetgroup_rmuser():
    """Remove a user from the targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetgroupname = request.form['targetgroupname']
    email           = request.form['email']

    # Check for required fields
    if not targetgroupname or not email:
        return "ERROR: The targetgroupname and email are required ", 417, {'Content-Type': 'text/plain'}

    # Targetgroup and user have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    u = get_user(email)
    if not u:
        return 'ERROR: no user "' + email + '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Now we can remove the user
    tg.rmuser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetgroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + email + '" removed from "' + targetgroupname + '"', 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/addusergroup', methods = ['POST'])
def targetgroup_addusergroup():
    """Add a usergroup in the targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetgroupname = request.form['targetgroupname']
    usergroupname   = request.form['usergroupname']

    # Check for required fields
    if not targetgroupname or not usergroupname:
        return "ERROR: The targetgroupname and usergroupname are required ", 417, {'Content-Type': 'text/plain'}

    # Targetgroup and usergroup have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    ug = get_usergroup(usergroupname)
    if not ug:
        return 'ERROR: no usergroup "' + usergroupname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Now we can add the usergroup
    tg.addusergroup(ug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetgroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + usergroupname + '" added to "' + targetgroupname + '"', 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/rmusergroup', methods = ['POST'])
def targetgroup_rmusergroup():
    """Remove a usergroup from the targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetgroupname = request.form['targetgroupname']
    usergroupname   = request.form['usergroupname']

    # Check for required fields
    if not targetgroupname or not usergroupname:
        return "ERROR: The targetgroupname and usergroupname are required ", 417, {'Content-Type': 'text/plain'}

    # Targetgroup and usergroup have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    ug = get_usergroup(usergroupname)
    if not ug:
        return 'ERROR: no usergroup "' + usergroupname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Now we can remove the usergroup
    tg.rmusergroup(ug)
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetgroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + usergroupname + '" removed from "' + targetgroupname + '"', 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/addtargetgroup', methods = ['POST'])
def targetgroup_addtargetgroup():
    """Add a targetgroup (subtargetgroup) in the targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetgroupname    = request.form['targetgroupname']
    subtargetgroupname = request.form['subtargetgroupname']

    # Check for required fields
    if not targetgroupname or not subtargetgroupname:
        return "ERROR: The targetgroupname and subtargetgroupname are required ", 417, {'Content-Type': 'text/plain'}

    # Targetgroup and subtargetgroup have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    subtg = get_targetgroup(subtargetgroupname)
    if not subtg:
        return 'ERROR: no targetgroup "' + subtargetgroupname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Now we can add the targetgroup
    tg.addtargetgroup(subtg)
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetgroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + subtargetgroupname + '" added to "' + targetgroupname + '"', 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/rmtargetgroup', methods = ['POST'])
def targetgroup_rmtargetgroup():
    """Remove a targetgroup (subtargetgroup) from the targetgroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    targetgroupname    = request.form['targetgroupname']
    subtargetgroupname = request.form['subtargetgroupname']

    # Check for required fields
    if not targetgroupname or not subtargetgroupname:
        return "ERROR: The targetgroupname and subtargetgroupname are required ", 417, {'Content-Type': 'text/plain'}

    # Targetgroup and subtargetgroup have to exist in database
    tg = get_targetgroup(targetgroupname)
    if not tg:
        return 'ERROR: no targetgroup "' + targetgroupname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    subtg = get_targetgroup(subtargetgroupname)
    if not subtg:
        return 'ERROR: no targetgroup "' + subtargetgroupname + '" in the database ', 417, {'Content-Type': 'text/plain'}

    # Now we can remove the targetgroup
    tg.rmtargetgroup(subtg)
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + targetgroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + subtargetgroupname + '" removed from "' + targetgroupname + '"', 200, {'Content-Type': 'text/plain'}

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

def get_targetgroup(targetgroupname):
    """Return the targetgroup with the given targetgroupname"""
    tg = db.session.query(targetgroup.Targetgroup).filter(
            targetgroup.Targetgroup.targetgroupname == targetgroupname).all()

    # Targetgroup must exist in database
    if tg:
        return tg[0]
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
    ug = db.session.query(usergroup.Usergroup).filter(
             usergroup.Usergroup.usergroupname == usergroupname).all()

    # Usergroup must exist in database
    if ug:
        return ug[0]
    else:
        return False
