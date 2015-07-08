# -*-coding:Utf-8 -*-

"""Contains functions which make requests to the server for target's management"""

import requests

url_passhport = "http://127.0.0.1:5000/"


def list():
    """Get the list of all targets"""
    url_list = url_passhport + "target/list"

    try:
        r = requests.get(url_list)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def search(param):
    """Get the list of targets that match the pattern"""
    url_search = url_passhport + "target/search/" + param['<pattern>']

    try:
        r = requests.get(url_search)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def create(param):
    """Target creation on passhportd via API"""
    url_create = url_passhport + "target/create"
    #TODO filter target_data by content (copy user behavior)
    target_data = {
        'targetname': param['<targetname>'],
        'hostname': param['<hostname>'],
        'comment': param['<comment>'],
        'sshoptions': param['<sshoptions>'],
        'port': param['<port>'],
        'servertype': param['<servertype>'],
        'autocommand': param['<autocommand>']}

    try:
        r = requests.post(url_create, data=target_data)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def show(param):
    """Get data about a target"""
    url_show = url_passhport + "target/show/" + param['<targetname>']

    try:
        r = requests.get(url_show)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def edit(param):
    """Target modification on passhportd via API"""
    url_edit = url_passhport + "target/edit"
    #TODO Filter content like we do for users
    target_data = {
        'targetname': param['<targetname>'],
        'new_targetname': param['<newtargetname>'],
        'new_hostname': param['<hostname>'],
        'new_comment': param['<comment>'],
        'new_sshoptions': param['<sshoptions>'],
        'new_port': param['<port>'],
        'new_servertype': param['<servertype>'],
        'new_autocommand': param['<autocommand>']}

    try:
        r = requests.post(url_edit, data=target_data)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def delete(param):
    """Target deletion on passhportd via API"""
    url_del = url_passhport + "target/del/" + param['<targetname>']

    try:
        r = requests.get(url_del)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def adduser(param):
    """Add a user in a target via API"""
    url_adduser = url_passhport + "target/adduser"
    target_user_data = {'targetname': param['<targetname>'],
            'email': param['<email>']}

    try:
        r = requests.post(url_adduser, data=target_user_data)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def rmuser(param):
    """Remove a user from a target via API"""
    url_rmuser = url_passhport + "target/rmuser"
    target_user_data = {'targetname': param['<targetname>'],
            'email': param['<email>']}

    try:
        r = requests.post(url_rmuser, data=target_user_data)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def addusergroup(param):
    """Add a usergroup in a target via API"""
    target_usergroup_data = {
        'targetname': param['<targetname>'],
        'usergroupname': param['<usergroupname>']}
    url_addusergroup = url_passhport + "target/addusergroup"

    try:
        r = requests.post(url_addusergroup, data=target_usergroup_data)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def rmusergroup(param):
    """Remove a usergroup from a target via API"""
    target_usergroup_data = {
        'targetname': param['<targetname>'],
        'usergroupname': param['<usergroupname>']}
    url_rmusergroup = url_passhport + "target/rmusergroup"

    try:
        r = requests.post(url_rmusergroup, data=target_usergroup_data)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1
