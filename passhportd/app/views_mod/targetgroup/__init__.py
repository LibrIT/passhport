# -*-coding:Utf-8 -*-

from app            import app, db
from flask          import request
from app.models_mod import targetgroup

@app.route("/targetgroup/list")
def targetgroup_list():
    """Return the targetgroup list of database"""
    result = []
    query  = db.session.query(targetgroup.Targetgroup.name).order_by(targetgroup. Targetgroup.name)

    for row in query.all():
        result.append(str(row[0].encode('utf8')))

    if not result:
        return "No targetgroup in database.\n", 200, {'Content-Type': 'text/plain'}

    return "\n".join(result), 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/search/<pattern>')
def targetgroup_search(pattern):
    """Return a list of targetgroups that match the given pattern"""
    result = []
    query  = db.session.query(targetgroup.Targetgroup.name)\
            .filter(targetgroup.Targetgroup.name.like('%' + pattern + '%'))

    for row in query.all():
        result.append(str(row[0]).encode('utf8'))

    if not result:
        return 'No targetgroup matching the pattern "' + pattern + '" found.\n', 200, {'Content-Type': 'text/plain'}

    return '\n'.join(result), 200, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/show/<targetgroupname>')
def targetgroup_show(targetgroupname):
    """Return all data about a targetgroup"""
    targetgroup_data = targetgroup.Targetgroup.query.filter_by(name = targetgroupname).first()

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
    query = db.session.query(targetgroup.Targetgroup.name)\
        .filter(targetgroup.Targetgroup.name.like(targetgroupname))

    # Normally only one row
    for row in query.all():
        if str(row[0]) == targetgroupname:
            return 'ERROR: The targetgroupname "' + targetgroupname + '" is already used by another targetgroup ', 417, {'Content-Type': 'text/plain'}

    t = targetgroup.Targetgroup(
            name    = targetgroupname,
            comment = comment)
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

    toupdate = db.session.query(targetgroup.Targetgroup).filter_by(name = targetgroupname)

    # Let's modify only relevent fields
    if new_comment:
        toupdate.update({'comment': str(new_comment).encode('utf8')})
    if new_targetgroupname:
        toupdate.update({'name': str(new_targetgroupname).encode('utf8')})

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
    query = db.session.query(targetgroup.Targetgroup.name)\
            .filter(targetgroup.Targetgroup.name.like(targetgroupname))

    # Normally only one row
    for row in query.all():
        if str(row[0]) == targetgroupname:
            db.session.query(targetgroup.Targetgroup).filter(targetgroup.Targetgroup.name == targetgroupname).delete()

            try:
                db.session.commit()
            except exc.SQLAlchemyError:
                return 'ERROR: "' + targetgroupname + '" -> ' + e.message + '\n', 409, {'Content-Type': 'text/plain'}

            return 'OK: "' + targetgroupname + '" -> deleted' + '\n', 200, {'Content-Type': 'text/plain'}

    return 'ERROR: No targetgroup with the name "' + targetgroupname + '" in the database.\n', 417, {'Content-Type': 'text/plain'}

@app.route('/targetgroup/adduser/', methods=['GET'])
def targetgroup_adduser():
    #TODO
    print  request.args.get('username')
    print  request.args.get('targetgroupname')
    return "adduser"

@app.route('/targetgroup/rmuser/', methods=['GET'])
def targetgroup_rmuser():
    #TODO
    print  request.args.get('username')
    print  request.args.get('targetgroupname')
    return "rmuser"

@app.route('/targetgroup/addtarget', methods=['GET'])
def targetgroup_addtarget():
    #TODO
    print  request.args.get('targetname')
    print  request.args.get('targetgroupname')
    return "addtarget"

@app.route('/targetgroup/rmtarget', methods=['GET'])
def targetgroup_rmtarget():
    #TODO
    print  request.args.get('targetname')
    print  request.args.get('targetgroupname')
    return "rmtarget"

@app.route('/targetgroup/addusergroup', methods=['GET'])
def targetgroup_addgroup():
    #TODO
    print  request.args.get('groupname')
    print  request.args.get('targetgroupname')
    return "addusergroup"

@app.route('/targetgroup/rmusergroup', methods=['GET'])
def targetgroup_rmgroup():
    #TODO
    print  request.args.get('groupname')
    print  request.args.get('targetgroupname')
    return "rmusergroup"

@app.route('/targetgroup/addtargetgroup', methods=['GET'])
def targetgroup_addtargetgroup():
    #TODO
    print  request.args.get('subtargetgroupname')
    print  request.args.get('targetgroupname')
    return "addtargetgroup"

@app.route('/targetgroup/rmtargetgroup', methods=['GET'])
def targetgroup_rmtargetgroup():
    #TODO
    print  request.args.get('subtargetgroupname')
    print  request.args.get('targetgroupname')
    return "rmtargetgroup"
