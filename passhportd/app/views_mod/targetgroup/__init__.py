from app import app

@app.route("/targetgroup/list")
def targetgroup_list():
    #TODO
    return "list of targetgroups"

@app.route('/targetgroup/search/<pattern>')
def targetgroup_search(pattern):
    #TODO
    return "pattern"

@app.route('/targetgroup/show/<targetgroupname>')
def targetgroup_show(targetgroupname):
    #TODO
    return "pattern"

@app.route('/targetgroup/create/', methods=['POST'])
def targetgroup_create():
    #TODO
    print  request.args.get('targetgroupname')
    print  request.args.get('anotherarg0')
    print  request.args.get('anotherarg1')
    print  request.args.get('anotherarg2')
    return "create"

@app.route('/targetgroup/edit/', methods=['POST'])
def targetgroup_edit():
    #TODO
    print  request.args.get('targetgroupname')
    print  request.args.get('anotherarg0')
    print  request.args.get('anotherarg1')
    print  request.args.get('anotherarg2')
    return "edit"

@app.route('/targetgroup/del/<usergroupname>')
def targetgroup_del(targetgroupname):
    #TODO
    return "delete"

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

