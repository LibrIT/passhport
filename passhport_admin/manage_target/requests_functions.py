# -*-coding:Utf-8 -*-

"""Contains functions which make requests to the server for target's management"""

import requests

url_passhport = "http://127.0.0.1:5000/"

def requests_target_list():
    """Get the list of all targets"""
    url_list = url_passhport + "target/list"

    try:
        r = requests.get(url_list)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_target_search(pattern):
    """Get the list of targets that match the pattern"""
    url_search = url_passhport + "target/search/" + pattern

    try:
        r = requests.get(url_search)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_target_create(targetname, hostname, comment, sshoptions, port, servertype, autocommand):
    """Target creation on passhportd via API"""
    target_data = {'targetname': targetname, 'hostname': hostname, 'comment': comment, 'sshoptions': sshoptions, 'port': port, 'servertype': servertype, 'autocommand': autocommand}
    url_create = url_passhport + "target/create"

    try:
        r = requests.post(url_create, data = target_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_target_show(targetname):
    """Get data about a target"""
    url_show = url_passhport + "target/show/" + targetname

    try:
        r = requests.get(url_show)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_target_show_users(targetname):
    """Get data about a target and its user list"""
    url_show_users = url_passhport + "target/show_users/" + targetname

    try:
        r = requests.get(url_show_users)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_target_show_usergroups(targetname):
    """Get data about a target and its usergroup list"""
    url_show_usergroups = url_passhport + "target/show_usergroups/" + targetname

    try:
        r = requests.get(url_show_usergroups)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_target_edit(targetname, new_targetname, new_hostname, new_comment, new_sshoptions, new_port, new_servertype, new_autocommand):
    """Target modification on passhportd via API"""
    target_data = {'targetname': targetname, 'new_targetname': new_targetname, 'new_hostname': new_hostname, 'new_comment': new_comment, 'new_sshoptions': new_sshoptions, 'new_port': new_port, 'new_servertype': new_servertype, 'new_autocommand': new_autocommand}
    url_edit = url_passhport + "target/edit"

    try:
        r = requests.post(url_edit, data = target_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_target_del(targetname):
    """Target deletion on passhportd via API"""
    url_del = url_passhport + "target/del/" + targetname

    try:
        r = requests.get(url_del)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_target_adduser(email, targetname):
    """Add a user in a target via API"""
    target_user_data = {'targetname': targetname, 'email': email}
    url_adduser = url_passhport + "target/adduser"

    try:
        r = requests.post(url_adduser, data = target_user_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_target_rmuser(email, targetname):
    """Remove a user from a target via API"""
    target_user_data = {'targetname': targetname, 'email': email}
    url_rmuser = url_passhport + "target/rmuser"

    try:
        r = requests.post(url_rmuser, data = target_user_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_target_addusergroup(usergroupname, targetname):
    """Add a usergroup in a target via API"""
    target_usergroup_data = {'targetname': targetname, 'usergroupname': usergroupname}
    url_addusergroup = url_passhport + "target/addusergroup"

    try:
        r = requests.post(url_addusergroup, data = target_usergroup_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_target_rmusergroup(usergroupname, targetname):
    """Remove a usergroup from a target via API"""
    target_usergroup_data = {'targetname': targetname, 'usergroupname': usergroupname}
    url_rmusergroup = url_passhport + "target/rmusergroup"

    try:
        r = requests.post(url_rmusergroup, data = target_usergroup_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1
