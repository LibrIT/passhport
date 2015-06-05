from flask          import request
from sqlalchemy     import exc
from sqlalchemy.orm import sessionmaker
from app            import app, db
from app.models_mod import user

@app.route('/user/list')
def user_list():
    """
    Return the users list from database query
    """
    result = ""
    for row in db.session.query(user.User.username).order_by(user.User.username):
        result = result + str(row[0]).encode('utf8')+"\n"
    return result


@app.route('/user/search/<pattern>')
def user_search(pattern):
    """
    To check
        Empty pattern
        pattern not in db
        Specific characters
        upper and lowercases
    """
    result = ""
    query = db.session.query( user.User.username )\
            .filter(user.User.username.like('%'+pattern+'%'))

    for row in query.all():
        result = result + str(row[0]).encode('utf8')+"\n"
    return result


@app.route('/user/show/<username>')
def user_show(username):
    """
    To check
        Empty pattern
        pattern not in db
        Specific characters
        upper and lowercases
    """
    u = user.User.query.filter_by(username=username).first()
    userdata=str(u)
    return userdata


@app.route('/user/create', methods=['POST'])
def user_create():
    """
    To check
        Empty fields,
        Already existing field,
        The access is well a POST
        The database add / commit has been successful
        #TODO Check if username / email / sshkey already exist
    """
    # Only POST data are handled
    if request.method != 'POST':
        return "POST Method is mandatory\n"

    # Simplification for the reading
    username= request.form['username']
    email   = request.form['email']
    sshkey  = request.form['sshkey']
    comment = request.form['comment']
    
    # Check for mandatory fields
    if len(username) == 0 | len(sshkey) == 0:
        return "ERROR: username and sshkey are mandatory\n"

    u = user.User(
            username= username,
            email   = email,
            sshkey  = sshkey,
            comment = comment)
    db.session.add(u)

    # Try to add the user on the databse
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return "ERROR: " + e.message + "\n"

    return "OK: " + username + "\n"


@app.route('/user/edit', methods=['POST'])
def user_edit():
    # Only POST data are handled
    if request.method != 'POST':
        return "POST Method is mandatory\n"

    # Simplification for the reading
    username    = request.form['username']
    newusername = request.form['newusername']
    email       = request.form['email']
    sshkey      = request.form['sshkey']
    comment     = request.form['comment']
    
    # Old username is mandatory to modify the right user
    if len(username) != 0:
        toupdate = db.session.query(user.User).filter_by(username=username)
    else:
        return "ERROR: username is mandatory\n"

    # Let's modify only revelent fields
    try:
        if len(newusername) != 0:
            toupdate.update({"username": str(newusername).encode('utf8')})
            db.session.commit()
        if len(email) != 0:
            toupdate.update({"email": str(email).encode('utf8')})
            db.session.commit()
        if len(sshkey) != 0:
            toupdate.update({"sshkey": str(sshkey).encode('utf8')})
            db.session.commit()
        if len(comment) != 0:
            toupdate.update({"comment": str(comment).encode('utf8')})
            db.session.commit()
    except exc.SQLAlchemyError:
        return "ERROR: " + exc

    return "OK: " + username + "\n"

@app.route('/user/del/<username>')
def user_del(username):
    """
    To check
        User exist
        Delete is ok
    """
    db.session.query(user.User).filter(user.User.username == username).delete()
    db.session.commit()
    return "deleted\n"

