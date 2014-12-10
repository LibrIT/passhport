#!/usr/bin/env python

from flask import Blueprint
target = Blueprint('target', __name__)

@target.route("/target/list")
def target_list():
    #TODO  
    return "list of accounts"

@target.route('/target/search/<pattern>')
def target_search(pattern):
    #TODO
    return """pattern"""

@target.route('/target/show/<username>')
def target_show(username):
    #TODO
    return """pattern"""

@target.route('/target/create/', methods=['POST'])
def target_create():
    #TODO
    print  request.args.get('target')
    print  request.args.get('anotherarg0')
    print  request.args.get('anotherarg1')
    print  request.args.get('anotherarg2')
    return """create"""

@target.route('/target/edit/', methods=['POST'])
def target_edit():
    #TODO
    print  request.args.get('target')
    print  request.args.get('anotherarg0')
    print  request.args.get('anotherarg1')
    print  request.args.get('anotherarg2')
    return """edit"""

@target.route('/target/del/<username>')
def target_edit(username):
    #TODO
    return """delete"""

@target.route('/target/editcommand/',methods=['POST'])
def target_editcommand():
    #TODO
    print  request.args.get('target')
    print  request.args.get('command')
    return """editcommand"""

@target.route('/target/adduser/',methods=['POST'])
def target_adduser():
    #TODO
    print request.args.get('username')
    print request.args.get('target')
    return """adduser"""

@target.route('/target/rmuser/',methods=['POST'])
def target_rmuser():
    #TODO
    print request.args.get('username')
    print request.args.get('target')
    return """adduser"""

@target.route('/target/rmuser/',methods=['POST'])
def target_rmuser():
    #TODO
    print request.args.get('username')
    print request.args.get('target')
    return """rmuser"""

@target.route('/target/addusergroup/',methods=['POST'])
def target_addusergroup():
    #TODO
    print request.args.get('groupname')
    print request.args.get('target')
    return """addusergroup"""

@target.route('/target/rmusergroup/',methods=['POST'])
def target_rmusergroup():
    #TODO
    print request.args.get('groupname')
    print request.args.get('target')
    return """rmusergroup"""

