#!/usr/bin/env python

from flask import Blueprint
usergroup = Blueprint('usergroup', __name__)

@usergroup.route('/usergroup/list')
def usergroup_list():
    #todo   
    return """gtiti\ngtoto\ngtutu"""

@usergroup.route('/usergroup/search/<pattern>')
def usergroup_search(pattern):
    #TODO
    return """pattern"""

@usergroup.route('/usergroup/show/<usergroupname>')
def usergroup_show(usergroupname):
    #TODO
    return """pattern"""

@usergroup.route('/usergroup/create/', methods=['POST'])
def usergroup_create():
    #TODO
    print  request.args.get('usergroupname')
    print  request.args.get('anotherarg0')
    print  request.args.get('anotherarg1')
    print  request.args.get('anotherarg2')
    return """create"""

@usergroup.route('/usergroup/edit/', methods=['POST'])
def usergroup_edit():
    #TODO
    print  request.args.get('usergroupname')
    print  request.args.get('anotherarg0')
    print  request.args.get('anotherarg1')
    print  request.args.get('anotherarg2')
    return """edit"""

@usergroup.route('/usergroup/del/<usergroupname>')
def usergroup_del(usergroupname):
    #TODO
    return """delete"""

@usergroup.route('/usergroup/adduser/', methods=['GET'])
def usergroup_adduser():
    #TODO
    print  request.args.get('username')
    print  request.args.get('groupname')
    return """adduser"""

@usergroup.route('/usergroup/rmuser/', methods=['GET'])
def usergroup_rmuser():
    #TODO
    print  request.args.get('username')
    print  request.args.get('groupname')
    return """rmuser"""

@usergroup.route('/usergroup/addtarget', methods=['GET'])
def usergroup_addtarget():
    #TODO
    print  request.args.get('targetname')
    print  request.args.get('groupname')
    return """addtarget"""

@usergroup.route('/usergroup/rmtarget', methods=['GET'])
def usergroup_rmtarget():
    #TODO
    print  request.args.get('targetname')
    print  request.args.get('groupname')
    return """rmtarget"""

@usergroup.route('/usergroup/addgroup', methods=['GET'])
def usergroup_addgroup():
    #TODO
    print  request.args.get('subgroup')
    print  request.args.get('groupname')
    return """addgroup"""

@usergroup.route('/usergroup/rmgroup', methods=['GET'])
def usergroup_rmgroup():
    #TODO
    print  request.args.get('subgroup')
    print  request.args.get('groupname')
    return """rmgroup"""

@usergroup.route('/usergroup/addtargetgroup', methods=['GET'])
def usergroup_addtargetgroup():
    #TODO
    print  request.args.get('targetgroupname')
    print  request.args.get('groupname')
    return """addtargetgroup"""

@usergroup.route('/usergroup/rmtargetgroup', methods=['GET'])
def usergroup_rmtargetgroup():
    #TODO
    print  request.args.get('targetgroupname')
    print  request.args.get('groupname')
    return """rmtargetgroup"""

