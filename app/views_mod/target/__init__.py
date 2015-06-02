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
    """
    Return the targets list from database query
    """
    result = ""
    for row in db.session.query( target.Target.targetname )\
            .order_by( target.Target.targetname ):
        result = result + str(row[0]).encode('utf8')+"""\n"""
    return result

    return "list of accounts"


@app.route('/target/search/<pattern>')
def target_search(pattern):
    """
    To check
        Empty pattern
        pattern not in db
        Specific characters
        upper and lowercases
    """
    result = ""
    query = db.session.query( target.Target.targetname )\
            .filter(target.Target.targetname.like('%'+pattern+'%'))

    for row in query.all():
        result = result + str(row[0]).encode('utf8')+"""\n"""
    return result


@app.route('/target/show/<targetname>')
def target_show(targetname):
    """
    To check
        Empty pattern
        pattern not in db
        Specific characters
        upper and lowercases
    """
    t = target.Target.query.filter_by(targetname=targetname).first()
    targetdata=str(t)
    return targetdata


@app.route('/target/create', methods=['POST'])
def target_create():
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
    targetname  = request.form['targetname']
    hostname    = request.form['hostname']
    port        = request.form['port']
    sshoptions  = request.form['sshoptions']
    servertype  = request.form['servertype']
    autocommand = request.form['autocommand']
    comment     = request.form['comment']
    
    # Check for mandatory fields
    if len(targetname) <= 0 | len(hostname) <= 0:
        return """ERROR: targetname and hostname are mandatory\n"""

    if len( port ) == 0:
        port = 22

    t = target.Target(
            targetname  = targetname,
            hostname    = hostname,
            port        = port,
            sshoptions  = sshoptions,
            servertype  = servertype,
            autocommand = autocommand,
            comment     = comment)
    db.session.add(t)

    # Try to add the target on the databse
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return """ERROR: """ + exc + """\n"""

    return """OK: """ + targetname + """\n"""


@app.route('/target/edit/', methods=['POST'])
def target_edit():
    """ Certainly this should be handled by the ORM... YOLO """
    # Only POST data are handled
    if request.method != 'POST':
        return """POST Method is mandatory\n"""

    # Simplification for the reading
    targetname      = request.form['targetname']
    newtargetname   = request.form['newtargetname']
    hostname        = request.form['hostname']
    port            = request.form['port']
    sshoptions      = request.form['sshoptions']
    servertype      = request.form['servertype']
    autocommand     = request.form['autocommand']
    comment         = request.form['comment']
    
    # Old targetname is mandatory to modify the right target
    if len(targetname) > 0:
        toupdate = db.session.query(target.Target). \
                filter_by(targetname=targetname)
    else:
        return """ERROR: targetname is mandatory\n"""

    # Let's modify only revelent fields
    if len(newtargetname) > 0:
        toupdate.update({"targetname": str(newtargetname).encode('utf8')})
    if len(hostname) > 0:
        toupdate.update({"hostname": str(hostname).encode('utf8')})
    if len(str(port)) > 0:
        toupdate.update({"port": port})
    if len(sshoptions) > 0:
        toupdate.update({"sshoptions": str(sshoptions).encode('utf8')})
    if len(severtype) > 0:
        toupdate.update({"servertype": str(servertype).encode('utf8')})
    if len(autocommand) > 0:
        toupdate.update({"autocommand": str(autocommand).encode('utf8')})
    if len(comment) > 0:
        toupdate.update({"comment": str(comment).encode('utf8')})
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return """ERROR: """ + exc

    return """OK: """ + targetname + """\n"""


@app.route('/target/del/<targetname>')
def target_del(targetname):
    """
    To check
        Target exist
        Delete is ok
    """
    if len(targetname) > 0:
        db.session.query(target.Target). \
            filter(target.Target.targetname == targetname).delete()
    else:
        return """ERROR: targetname is mandatory\n"""

    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return """ERROR: """ + exc

    return """Deleted\n"""


@app.route('/target/adduser',methods=['POST'])
def target_adduser():
    # Only POST data are handled
    if request.method != 'POST':
        return """POST Method is mandatory\n"""

    # Simplification for the reading
    targetname  = request.form['targetname']
    username    = request.form['username']
   
    if len(targetname) <= 0 or len(username) <= 0 :
        return """ERROR: targetname and username are mandatory\n"""

    # Target and user have to exist in database
    t = get_target(targetname)
    if t == False:
        return """Error: target does not exist\n"""

    u = get_user(username)
    if u == False:
        return """Error: user does not exist\n"""

    # Now we can add the user
    t.adduser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return """ERROR: """ + exc

    return username + """ added to """ + targetname + """\n"""


@app.route('/target/rmuser',methods=['POST'])
def target_rmuser():
    # Only POST data are handled
    if request.method != 'POST':
        return """POST Method is mandatory\n"""

    # Simplification for the reading
    targetname  = request.form['targetname']
    username    = request.form['username']

    if len(targetname) <= 0 or len(username) <= 0 :
        return """ERROR: targetname and username are mandatory\n"""

    # Target and user have to exist in database
    t = get_target(targetname)
    if t == False:
        return """Error: target does not exist\n"""

    u = get_user(username)
    if u == False:
        return """Error: user does not exist\n"""

    # We can remove the user from this target
    t.rmuser(u)
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return """ERROR: """ + exc

    return username + """ removed from """ + targetname + """\n"""


@app.route('/target/addusergroup/',methods=['POST'])
def target_addusergroup():
    """ Has to be tested """
    # Only POST data are handled
    if request.method != 'POST':
        return """POST Method is mandatory\n"""

    # Simplification for the reading
    targetname      = request.form['targetname']
    usergroupname   = request.form['usergroupname']
   
    if len(targetname) <= 0 or len(usergroupname) <= 0 :
        return """ERROR: targetname and usergroupname are mandatory\n"""

    # Target and user have to exist in database
    t = get_target(targetname)
    if t == False:
        return """Error: target does not exist\n"""

    g = get_ugroup(usergroupname)
    if g == False:
        return """Error: usergroup does not exist\n"""

    # Now we can add the user
    t.addusergroup(g)
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return """ERROR: """ + exc

    return usergroupname + """ added to """ + targetname + """\n"""


@app.route('/target/rmusergroup/',methods=['POST'])
def target_rmusergroup():
    """ Has to be tested """
    # Only POST data are handled
    if request.method != 'POST':
        return """POST Method is mandatory\n"""

    # Simplification for the reading
    targetname      = request.form['targetname']
    usergroupname   = request.form['usergroupname']
   
    if len(targetname) <= 0 or len(usergroupname) <= 0 :
        return """ERROR: targetname and usergroupname are mandatory\n"""

    # Target and user have to exist in database
    t = get_target(targetname)
    if t == False:
        return """Error: target does not exist\n"""

    g = get_ugroup(usergroupname)
    if g == False:
        return """Error: usergroup does not exist\n"""

    # Now we can add the user
    t.rmusergroup(g)
    try:
        db.session.commit()
    except exc.SQLAlchemyError:
        return """ERROR: """ + exc

    return usergroupname + """ added to """ + targetname + """\n"""



# Utils
""" Return a Target object from the target name"""
def get_target(targetname):
    t = db.session.query(target.Target).filter(
            target.Target.targetname == targetname).all()
    # Target must exist in database
    if len(t) > 0:
        return t[0]
    else:
        return False

""" Return a User object from the user name"""
def get_user(username):
    u = db.session.query(user.User).filter(
             user.User.username == username).all()
    # User must exist in database
    if len(u) > 0:
        return u[0]
    else:
        return False
    
""" Return a Usergroup object from the usergroup name"""
def get_usergroup(usergroupname):
    g = db.session.query(usergroup.Usergroup).filter(
             usergroup.Usergroup.usergroupname == usergroupname).all()
    # Usergroup must exist in database
    if len(g) > 0:
        return g[0]
    else:
        return False
    

