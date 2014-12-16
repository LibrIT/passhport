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
    """
    Return the usergroups list from database query
    """
    result = ""
    for row in db.session.query(usergroup.Usergroup.groupname)\
            .order_by(usergroup.Usergroup.groupname):
        result = result + str(row[0]).encode('utf8')+"""\n"""
    return result

@app.route('/usergroup/search/<pattern>')
def usergroup_search(pattern):
    """
    To check
        Empty pattern
        pattern not in db
        Specific characters
        upper and lowercases
    """
    result = ""
    query = db.session.query(usergroup.Usergroup.groupname)\
            .filter(usergroup.Usergroup.groupname.like('%'+pattern+'%'))

    for row in query.all():
        result = result + str(row[0]).encode('utf8')+"""\n"""
    return result


@app.route('/usergroup/show/<groupname>')
def usergroup_show(groupname):
    """
    To check
        Empty pattern
        pattern not in db
        Specific characters
        upper and lowercases
    """
    return str(usergroup.Usergroup.query. \
            filter_by(groupname=groupname).first())


@app.route('/usergroup/create/', methods=['POST'])
def usergroup_create():
    """
    To check
        Empty fields,
        Already existing field,
        The access is well a POST
        The database add / commit has been successful
        #TODO Check if targetname already exist 
    """
    # Only POST data are handled
    if request.method != 'POST':
        return """POST Method is mandatory\n"""

    # Simplification for the reading
    groupname  = request.form['groupname']
    comment    = request.form['comment']
    
    # Check for mandatory fields
    if len(groupname) <= 0 :
        return """ERROR: groupname is mandatory\n"""

    g = usergroup.Usergroup(
            groupname  = groupname,
            comment     = comment)
    db.session.add(g)

    # Try to add the target on the databse
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return """ERROR: """ + exc + """\n"""

    return """OK: """ + groupname + """\n"""

@app.route('/usergroup/edit/', methods=['POST'])
def usergroup_edit():
    """ Certainly this should be handled by the ORM... YOLO """
    # Only POST data are handled
    if request.method != 'POST':
        return """POST Method is mandatory\n"""

    # Simplification for the reading
    groupname   = request.form['groupname']
    newgroupname= request.form['newgroupname']
    comment     = request.form['comment']
    
    # Old groupname is mandatory to modify the right usergroup
    if len(groupname) > 0:
        toupdate = db.session.query(usergroup.Usergroup). \
                filter_by(groupname=groupname)
    else:
        return """ERROR: groupname is mandatory\n"""

    # Let's modify only revelent fields
    if len(newgroupname) > 0:
        toupdate.update({"groupname": str(newgroupname).encode('utf8')})
    if len(comment) > 0:
        toupdate.update({"comment": str(comment).encode('utf8')})

    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return """ERROR: """ + exc

    return """OK: """ + groupname + """\n"""


@app.route('/usergroup/del/<groupname>')
def usergroup_del(groupname):
    """
    To check
        groupname exist
        Delete is ok
    """
    if len(groupname) > 0:
        db.session.query(usergroup.Usergroup). \
            filter(usergroup.Usergroup.groupname == groupname).delete()
    else:
        return """ERROR: groupname is mandatory\n"""

    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return """ERROR: """ + exc

    return """Deleted\n"""


@app.route('/usergroup/adduser/', methods=['GET'])
def usergroup_adduser():
    # Only POST data are handled
    if request.method != 'POST':
        return """POST Method is mandatory\n"""

    # Simplification for the reading
    groupname   = request.form['groupname']
    username    = request.form['username']
   
    if len(groupname) <= 0 or len(username) <= 0 :
        return """ERROR: groupname and username are mandatory\n"""

    # Target and user have to exist in database
    g = get_target(groupname)
    if t == False:
        return """Error: usergroup does not exist\n"""

    u = get_user(username)
    if u == False:
        return """Error: user does not exist\n"""

    # Now we can add the user
    t.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return """ERROR: """ + exc

    return username + """ added to """ + groupname + """\n"""

    #TODO
    print  request.args.get('username')
    print  request.args.get('groupname')
    return """adduser"""

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
    return """addgroup"""

@app.route('/usergroup/rmusergroup', methods=['GET'])
def usergroup_rmgroup():
    #TODO
    print  request.args.get('subgroup')
    print  request.args.get('groupname')
    return """rmgroup"""

#@app.route('/usergroup/addtarget', methods=['GET'])
#def usergroup_addtarget():
#    #TODO
#    print  request.args.get('targetname')
#    print  request.args.get('groupname')
#    return """addtarget"""
#
#@app.route('/usergroup/rmtarget', methods=['GET'])
#def usergroup_rmtarget():
#    #TODO
#    print  request.args.get('targetname')
#    print  request.args.get('groupname')
#    return """rmtarget"""
#@app.route('/usergroup/addtargetgroup', methods=['GET'])
#def usergroup_addtargetgroup():
#    #TODO
#    print  request.args.get('targetgroupname')
#    print  request.args.get('groupname')
#    return """addtargetgroup"""
#
#@app.route('/usergroup/rmtargetgroup', methods=['GET'])
#def usergroup_rmtargetgroup():
#    #TODO
#    print  request.args.get('targetgroupname')
#    print  request.args.get('groupname')
#    return """rmtargetgroup"""
#
