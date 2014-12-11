from app import app

@app.route("/target/list")
def target_list():
    #TODO  
    return "list of accounts"

@app.route('/target/search/<pattern>')
def target_search(pattern):
    #TODO
    return """pattern"""

@app.route('/target/show/<username>')
def target_show(username):
    #TODO
    return """pattern"""

@app.route('/target/create/', methods=['POST'])
def target_create():
    #TODO
    print  request.args.get('target')
    print  request.args.get('anotherarg0')
    print  request.args.get('anotherarg1')
    print  request.args.get('anotherarg2')
    return """create"""

@app.route('/target/edit/', methods=['POST'])
def target_edit():
    #TODO
    print  request.args.get('target')
    print  request.args.get('anotherarg0')
    print  request.args.get('anotherarg1')
    print  request.args.get('anotherarg2')
    return """edit"""

@app.route('/target/del/<username>')
def target_del(username):
    #TODO
    return """delete"""

@app.route('/target/editcommand/',methods=['POST'])
def target_editcommand():
    #TODO
    print  request.args.get('target')
    print  request.args.get('command')
    return """editcommand"""

@app.route('/target/adduser/',methods=['POST'])
def target_adduser():
    #TODO
    print request.args.get('username')
    print request.args.get('target')
    return """adduser"""

@app.route('/target/rmuser/',methods=['POST'])
def target_rmuser():
    #TODO
    print request.args.get('username')
    print request.args.get('target')
    return """rmuser"""

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

