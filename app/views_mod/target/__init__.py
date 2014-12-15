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
    
    # Old targetname is mandatory to modify the right user
    if len(targetname) > 0:
        toupdate = db.session.query(target.Target). \
                filter_by(targetname=targetname)
    else:
        return """ERROR: targetname is mandatory\n"""

    # Let's modify only revelent fields
    try:
        if len(newtargetname) != 0:
            toupdate.update({"targetname": str(newtargetname).encode('utf8')})
            db.session.commit()
        if len(hostname) != 0:
            toupdate.update({"hostname": str(hostname).encode('utf8')})
            db.session.commit()
        if len(str(port)) != 0:
            toupdate.update({"port": port})
            db.session.commit()
        if len(sshoptions) != 0:
            toupdate.update({"sshoptions": str(sshoptions).encode('utf8')})
            db.session.commit()
        if len(severtype) != 0:
            toupdate.update({"servertype": str(servertype).encode('utf8')})
            db.session.commit()
        if len(autocommand) != 0:
            toupdate.update({"autocommand": str(autocommand).encode('utf8')})
            db.session.commit()
        if len(comment) != 0:
            toupdate.update({"comment": str(comment).encode('utf8')})
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

    return """deleted\n"""


@app.route('/target/adduser',methods=['POST'])
def target_adduser():
    # Only POST data are handled
    if request.method != 'POST':
        return """POST Method is mandatory\n"""

    # Simplification for the reading
    targetname  = request.form['targetname']
    username    = request.form['username']
   
    # We check if both user and target  were sent
    if len(targetname) > 0 and len(username) > 0 :
        t = db.session.query(target.Target).filter(
                target.Target.targetname == targetname).all()
        u = db.session.query(user.User).filter(
                user.User.username == username).all()
    else:
        return """ERROR: targetname and username are mandatory\n"""

    # Target and user have to exist in database
    if len(t) > 0:
        t = t[0] # if there is a bug, we take the first targetname occurence
    else:
        return """Error: target does not exist\n"""
    
    if len(u) > 0:
        u = u[0]
    else:
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

    # We check if both user and target  were sent
    if len(targetname) > 0 and len(username) > 0 :
        t = db.session.query(target.Target).filter(
                target.Target.targetname == targetname).all()
        u = db.session.query(user.User).filter(
                user.User.username == username).all()
    else:
        return """ERROR: targetname and username are mandatory\n"""

    # Target and user have to exist in database
    if len(t) > 0:
        t = t[0] # if there is a bug, we take the first targetname occurence
    else:
        return """Error: target does not exist\n"""
    
    if len(u) > 0:
        u = u[0]
    else:
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
    #TODO
    print request.args.get('groupname')
    print request.args.get('target')
    return """addusergroup"""

@app.route('/target/rmusergroup/',methods=['POST'])
def target_rmusergroup():
    #TODO
    print request.args.get('groupname')
    print request.args.get('target')
    return """rmusergroup"""

