#!/usr/bin/env python

from flask import Blueprint
targetgroup = Blueprint('targetgroup', __name__)

@targetgroup.route("/targetgroup/list")
def targetgroup_list():
    #TODO
    return "list of targetgroups"

@targetgroup.route('/targetgroup/search/<pattern>')
def targetgroup_search(pattern):
    #TODO
    return """pattern"""

@targetgroup.route('/targetgroup/show/<targetgroupname>')
def targetgroup_show(targetgroupname):
    #TODO
    return """pattern"""

@targetgroup.route('/targetgroup/create/', methods=['POST'])
def targetgroup_create():
    #TODO
    print  request.args.get('targetgroupname')
    print  request.args.get('anotherarg0')
    print  request.args.get('anotherarg1')
    print  request.args.get('anotherarg2')
    return """create"""

@targetgroup.route('/targetgroup/edit/', methods=['POST'])
def targetgroup_edit():
    #TODO
    print  request.args.get('targetgroupname')
    print  request.args.get('anotherarg0')
    print  request.args.get('anotherarg1')
    print  request.args.get('anotherarg2')
    return """edit"""

@targetgroup.route('/targetgroup/del/<usergroupname>')
def targetgroup_edit(targetgroupname):
    #TODO
    return """delete"""

@targetgroup.route('/targetgroup/adduser/', methods=['GET'])
def targetgroup_adduser():
    #TODO
    print  request.args.get('username')
    print  request.args.get('targetgroupname')
    return """adduser"""

@targetgroup.route('/targetgroup/rmuser/', methods=['GET'])
def targetgroup_rmuser():
    #TODO
    print  request.args.get('username')
    print  request.args.get('targetgroupname')
    return """rmuser"""

@targetgroup.route('/targetgroup/addtarget', methods=['GET'])
def targetgroup_addtarget():
    #TODO
    print  request.args.get('targetname')
    print  request.args.get('targetgroupname')
    return """addtarget"""

@targetgroup.route('/targetgroup/rmtarget', methods=['GET'])
def targetgroup_rmtarget():
    #TODO
    print  request.args.get('targetname')
    print  request.args.get('targetgroupname')
    return """rmtarget"""

@targetgroup.route('/targetgroup/addusergroup', methods=['GET'])
def targetgroup_addgroup():
    #TODO
    print  request.args.get('groupname')
    print  request.args.get('targetgroupname')
    return """addusergroup"""

@targetgroup.route('/targetgroup/rmusergroup', methods=['GET'])
def targetgroup_rmgroup():
    #TODO
    print  request.args.get('groupname')
    print  request.args.get('targetgroupname')
    return """rmusergroup"""

@targetgroup.route('/targetgroup/addtargetgroup', methods=['GET'])
def targetgroup_addtargetgroup():
    #TODO
    print  request.args.get('subtargetgroupname')
    print  request.args.get('targetgroupname')
    return """addtargetgroup"""

@targetgroup.route('/targetgroup/rmtargetgroup', methods=['GET'])
def targetgroup_rmtargetgroup():
    #TODO
    print  request.args.get('subtargetgroupname')
    print  request.args.get('targetgroupname')
    return """rmtargetgroup"""

