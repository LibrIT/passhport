#!/usr/bin/env python

from flask import Blueprint
user = Blueprint('user', __name__)

@user.route('/user/list')
def user_list():
    #todo   
    return """titi\ntoto\ntutu"""

@user.route('/user/search/<pattern>')
def user_search(pattern):
    #TODO
    return """pattern"""

@user.route('/user/show/<username>')
def user_show(username):
    #TODO
    return """pattern"""

@user.route('/user/create/', methods=['POST'])
def user_create():
    #TODO
    print  request.args.get('username')
    print  request.args.get('anotherarg0')
    print  request.args.get('anotherarg1')
    print  request.args.get('anotherarg2')
    return """create"""

@user.route('/user/edit/', methods=['POST'])
def user_edit():
    #TODO
    print  request.args.get('username')
    print  request.args.get('anotherarg0')
    print  request.args.get('anotherarg1')
    print  request.args.get('anotherarg2')
    return """edit"""

@user.route('/user/del/<username>')
def user_del(username):
    #TODO
    return """delete"""

