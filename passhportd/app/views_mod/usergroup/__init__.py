# -*-coding:Utf-8 -*-

from app import app
from flask          import request
from sqlalchemy     import exc
from sqlalchemy.orm import sessionmaker
from app            import app, db
from app.models_mod import target
from app.models_mod import user
from app.models_mod import usergroup

@app.route('/usergroup/list')
def usergroup_list():
    """Return the usergroup list of database"""
    result = []
    query  = db.session.query(usergroup.Usergroup.usergroupname).order_by(usergroup.Usergroup.usergroupname)

    for row in query.all():
        result.append(str(row[0]).encode('utf8'))

    if not result:
        return "No usergroup in database.\n", 200, {'Content-Type': 'text/plain'}

    return '\n'.join(result), 200, {'Content-Type': 'text/plain'}

@app.route('/usergroup/search/<pattern>')
def usergroup_search(pattern):
    """Return a list of usergroups that match the given pattern"""
    """
    To check
        pattern not in db
        Specific characters
        upper and lowercases
    """

    result = []
    query  = db.session.query(usergroup.Usergroup.usergroupname)\
        .filter(usergroup.Usergroup.usergroupname.like('%' + pattern + '%'))

    for row in query.all():
        result.append(str(row[0]).encode('utf8'))

    if not result:
        return 'No usergroup matching the pattern "' + pattern + '" found.\n', 200, {'Content-Type': 'text/plain'}

    return '\n'.join(result), 200, {'Content-Type': 'text/plain'}

@app.route('/usergroup/show/<usergroupname>')
def usergroup_show(usergroupname):
    """Return all data about a usergroup"""
    """
    To check
        pattern not in db
        Specific characters
        upper and lowercases
    """

    usergroup_data = usergroup.Usergroup.query.filter_by(usergroupname = usergroupname).first()

    if usergroup_data is None:
        return 'ERROR: No usergroup with the name "' + usergroupname + '" in the database.\n', 417, {'Content-Type': 'text/plain'}

    return str(usergroup_data), 200, {'Content-Type': 'text/plain'}

@app.route('/usergroup/create', methods = ['POST'])
def usergroup_create():
    """Add a usergroup in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    usergroupname = request.form['usergroupname']
    comment       = request.form['comment']

    # Check for required fields
    if not usergroupname:
        return "ERROR: The usergroupname is required ", 417, {'Content-Type': 'text/plain'}

    # Check unicity for groupname
    query = db.session.query(usergroup.Usergroup.usergroupname)\
        .filter(usergroup.Usergroup.usergroupname.like(usergroupname))

    # Normally only one row
    for row in query.all():
        if str(row[0]) == usergroupname:
            return 'ERROR: The name "' + usergroupname + '" is already used by another user ', 417, {'Content-Type': 'text/plain'}

    g = usergroup.Usergroup(
            usergroupname  = usergroupname,
            comment        = comment)
    db.session.add(g)

    # Try to add the usergroup on the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + usergroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + usergroupname + '" -> created' + '\n', 200, {'Content-Type': 'text/plain'}

@app.route('/usergroup/edit', methods = ['POST'])
def usergroup_edit():
    """Edit a user in the database"""
    # Only POST data are handled
    if request.method != 'POST':
        return "ERROR: POST method is required ", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    usergroupname     = request.form['usergroupname']
    new_usergroupname = request.form['new_usergroupname']
    new_comment       = request.form['new_comment']

    toupdate = db.session.query(usergroup.Usergroup).filter_by(usergroupname = usergroupname)

    # Let's modify only relevent fields
    # Strangely the order is important, have to investigate why
    if new_comment:
        toupdate.update({"comment": str(new_comment).encode('utf8')})
    if new_usergroupname:
        toupdate.update({"usergroupname": str(new_usergroupname).encode('utf8')})

    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return 'ERROR: "' + usergroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

    return 'OK: "' + usergroupname + '" -> edited' + '\n', 200, {'Content-Type': 'text/plain'}

@app.route('/usergroup/del/<usergroupname>')
def usergroup_del(usergroupname):
    """Delete a user in the database"""
    if not usergroupname:
        return "ERROR: The groupname is required ", 417, {'Content-Type': 'text/plain'}

    # Check if the groupname exists
    query = db.session.query(usergroup.Usergroup.usergroupname)\
        .filter(usergroup.Usergroup.usergroupname.like(usergroupname))

    # Normally only one row
    for row in query.all():
        if str(row[0]) == usergroupname:
            db.session.query(usergroup.Usergroup).filter(usergroup.Usergroup.usergroupname == usergroupname).delete()

            try:
                db.session.commit()
            except exc.SQLAlchemyError, e:
                return 'ERROR: "' + usergroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

            return 'OK: "' + usergroupname + '" -> deleted' + '\n', 200, {'Content-Type': 'text/plain'}

    return 'ERROR: No usergroup with the name "' + usergroupname + '" in the database.\n', 417, {'Content-Type': 'text/plain'}

@app.route('/usergroup/adduser/', methods=['GET'])
def usergroup_adduser():
    # Only POST data are handled
    if request.method != 'POST':
        return "POST Method is mandatory\n"

    # Simplification for the reading
    usergroupname   = request.form['usergroupname']
    username        = request.form['username']

    if len(groupname) <= 0 or len(username) <= 0 :
        return "ERROR: groupname and username are mandatory\n"

    # Target and user have to exist in database
    g = get_target(groupname)
    if t == False:
        return "Error: usergroup does not exist\n"

    u = get_user(username)
    if u == False:
        return "Error: user does not exist\n"

    # Now we can add the user
    t.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return "ERROR: " + exc

    return username + " added to " + groupname + "\n"

    #TODO
    print  request.args.get('username')
    print  request.args.get('groupname')
    return "adduser"

@app.route('/usergroup/rmuser/', methods=['GET'])
def usergroup_rmuser():
    #TODO
    print  request.args.get('username')
    print  request.args.get('groupname')

@app.route('/usergroup/addusergroup', methods=['GET'])
def usergroup_addgroup():
    #TODO
    print  request.args.get('subgroup')
    print  request.args.get('groupname')
    return "addgroup"

@app.route('/usergroup/rmusergroup', methods=['GET'])
def usergroup_rmgroup():
    #TODO
    print  request.args.get('subgroup')
    print  request.args.get('groupname')
    return "rmgroup"

#@app.route('/usergroup/addtarget', methods=['GET'])
#def usergroup_addtarget():
#    #TODO
#    print  request.args.get('targetname')
#    print  request.args.get('groupname')
#    return "addtarget"
#
#@app.route('/usergroup/rmtarget', methods=['GET'])
#def usergroup_rmtarget():
#    #TODO
#    print  request.args.get('targetname')
#    print  request.args.get('groupname')
#    return "rmtarget"
#@app.route('/usergroup/addtargetgroup', methods=['GET'])
#def usergroup_addtargetgroup():
#    #TODO
#    print  request.args.get('targetgroupname')
#    print  request.args.get('groupname')
#    return "addtargetgroup"
#
#@app.route('/usergroup/rmtargetgroup', methods=['GET'])
#def usergroup_rmtargetgroup():
#    #TODO
#    print  request.args.get('targetgroupname')
#    print  request.args.get('groupname')
#    return "rmtargetgroup"
#
