# -*-coding:Utf-8 -*-

from flask          import request
from sqlalchemy     import exc
from sqlalchemy.orm import sessionmaker
from app            import app, db
from app.models_mod import user

@app.route('/user/list')
def user_list():
    """Return the users list from database query"""

    result = ""
    query = db.session.query(user.User.email).order_by(user.User.email)

    for row in query.all():
        result = result + str(row[0]).encode('utf8') + "\n"

    if result == "":
        return "No user in database.\n", 200, {'Content-Type': 'text/plain'}

    return result, 200, {'Content-Type': 'text/plain'}

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
    query = db.session.query(user.User.email)\
            .filter(user.User.email.like('%' + pattern + '%'))

    for row in query.all():
        result = result + str(row[0]).encode('utf8') + "\n"

    if result == "":
        return "ERROR: no user matching the pattern " + pattern + " found.\n", 404, {'Content-Type': 'text/plain'}

    return result, 200, {'Content-Type': 'text/plain'}

@app.route('/user/show/<email>')
def user_show(email):
    """
    To check
        Empty pattern
        pattern not in db
        Specific characters
        upper and lowercases
    """

    # check if email is empty
    if (len(email) == 0):
        return "ERROR: Email cannot be empty ", 417, {'Content-Type': 'text/plain'}

    u = user.User.query.filter_by(email = email).first()
    userdata = str(u)

    if userdata == "None":
        return "ERROR: No user with email " + email + " in the database.\n", 404, {'Content-Type': 'text/plain'}

    return userdata, 200, {'Content-Type': 'text/plain'}

@app.route('/user/create', methods=['POST'])
def user_create():
    """
    To check
        Empty fields,
        Already existing field,
        The access is well a POST
        The database add / commit has been successful
        #TODO Check if / email / sshkey already exist
    """

    # Only POST data are handled
    if request.method != 'POST':
        return "POST Method is mandatory\n", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    email   = request.form['email']
    sshkey  = request.form['sshkey']
    comment = request.form['comment']

    # Check for mandatory fields
    if (len(email) == 0) or (len(sshkey) == 0):
        return "ERROR: Email and SSHKey are mandatory\n", 417, {'Content-Type': 'text/plain'}

    # Check unicity for email
    result = ""
    query = db.session.query(user.User.email)\
        .filter(user.User.email.like(email))

    # normally only one row
    for row in query.all():
        if str(row[0]) == email:
            return "ERROR: the email " + email + " is already used by another user.\n", 417, {'Content-Type': 'text/plain'}

    # Check unicity for sshkey
    result = ""
    query = db.session.query(user.User.sshkey)\
        .filter(user.User.sshkey.like(sshkey))

    for row in query.all():
        if str(row[0]) == sshkey:
            return "ERROR: the SSHkey " + sshkey + " is already used by another user.\n", 417, {'Content-Type': 'text/plain'}

    u = user.User(
            email   = email,
            sshkey  = sshkey,
            comment = comment)
    db.session.add(u)

    # Try to add the user on the databse
    try:
        db.session.commit()
    except exc.SQLAlchemyError, e:
        return "ERROR: " + email + " -> " + e.message + "\n", 409, {'Content-Type': 'text/plain'}

    return "OK: " + email + " -> Created" + "\n", 200, {'Content-Type': 'text/plain'}

@app.route('/user/edit', methods=['POST'])
def user_edit():
    """Edit a user in the database"""

    # Only POST data are handled
    if request.method != 'POST':
        return "POST Method is mandatory\n", 405, {'Content-Type': 'text/plain'}

    # Simplification for the reading
    email       = request.form['email']
    new_email   = request.form['new_email']
    new_comment = request.form['new_comment']
    new_sshkey  = request.form['new_sshkey']

    # Old username is mandatory to modify the right user
    if len(email) != 0:
        toupdate = db.session.query(user.User).filter_by(email = email)
    else:
        return "ERROR: email is mandatory\n", 417, {'Content-Type': 'text/plain'}

    # Let’s modify only revelent fields
    try:
        if len(new_email) != 0:
            toupdate.update({"email": str(new_email).encode('utf8')})
            db.session.commit()
        if len(new_comment) != 0:
            toupdate.update({"comment": str(new_comment).encode('utf8')})
            db.session.commit()
        if len(new_sshkey) != 0:
            toupdate.update({"sshkey": str(new_sshkey).encode('utf8')})
            db.session.commit()
    except exc.SQLAlchemyError, e:
        return "ERROR: " + email + " -> " + e.message + "\n", 409, {'Content-Type': 'text/plain'}

    return "OK: User modified: " + email + "\n", 200, {'Content-Type': 'text/plain'}

@app.route('/user/del/<username>')
def user_del(username):
    """
    To check
        User exist
        Delete is ok
    """
    db.session.query(user.User).filter(user.User.username == username).delete()
    db.session.commit()
    return "Deleted: " + username + "\n", 200, {'Content-Type': 'text/plain'}
