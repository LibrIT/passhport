from flask          import request
from sqlalchemy     import exc
from app            import app, db
from app.models_mod import user

@app.route('/user/list')
def user_list():
    #TODO  
    return """titi\ntoto\ntutu"""

@app.route('/user/search/<pattern>')
def user_search(pattern):
    #TODO
    return """pattern"""

@app.route('/user/show/<username>')
def user_show(username):
    #TODO
    return """pattern"""

@app.route('/user/create', methods=['POST'])
def user_create():
    """
    Test to check
        Empty fields,
        Already existing field,
        The access is well a POST
        The database add / commit has been successful
        #TODO Check if username / email / sshkey already exist
    """

    if request.method == 'POST':
        username= request.form['username']
        email   = request.form['email']
        sshkey  = request.form['sshkey']
        comment = request.form['comment']

        # Setting the default output
        output = """OK: """ + request.form['username'] + """\n"""
        
        # Check for mandatory fields
        if len(username) == 0 | len(sshkey) == 0:
            output = """ERROR:username and sshkey are mandatory"""
        else:
            u = user.User(
                    username= username,
                    email   = email,
                    sshkey  = sshkey,
                    comment = comment)
            db.session.add(u)

            # Try to add the user on the databse
            try:
                db.session.commit()
            except exc.SQLAlchemyError:
                output = """ERROR:""" + exc

    else:
         output = """ERROR:MUST BE POST"""
            
    return output 

@app.route('/user/edit/', methods=['POST','GET'])
def user_edit():
    #TODO
    print  request.args.get('username')
    print  request.args.get('anotherarg0')
    print  request.args.get('anotherarg1')
    print  request.args.get('anotherarg2')
    return """edit"""

@app.route('/user/del/<username>')
def user_del(username):
    #TODO
    return """delete"""

