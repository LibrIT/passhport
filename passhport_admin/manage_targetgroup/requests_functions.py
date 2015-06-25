# -*-coding:Utf-8 -*-

"""Contains functions which make requests to the server for targetgroup's management"""

import requests

url_passhport = "http://127.0.0.1:5000/"

def requests_targetgroup_list():
    """Get the list of all targetgroups"""
    url_list = url_passhport + "targetgroup/list"

    try:
        r = requests.get(url_list)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_targetgroup_search(pattern):
    """Get the list of targetgroups that match the pattern"""
    url_search = url_passhport + "targetgroup/search/" + pattern

    try:
        r = requests.get(url_search)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_targetgroup_create(targetgroupname, comment):
    """Targetgroup creation on passhportd via API"""
    targetgroup_data = {'targetgroupname': targetgroupname, 'comment': comment}
    url_create = url_passhport + "targetgroup/create"

    try:
        r = requests.post(url_create, data = targetgroup_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_targetgroup_show(targetgroupname):
    """Get data about a targetgroup"""
    url_show = url_passhport + "targetgroup/show/" + targetgroupname

    try:
        r = requests.get(url_show)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_targetgroup_edit(targetgroupname, new_targetgroupname, new_comment):
    """Targetgroup modification on passhportd via API"""
    targetgroup_data = {'targetgroupname': targetgroupname, 'new_targetgroupname': new_targetgroupname, 'new_comment': new_comment}
    url_edit = url_passhport + "targetgroup/edit"

    try:
        r = requests.post(url_edit, data = targetgroup_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_targetgroup_del(targetgroupname):
    """Targetgroup deletion on passhportd via API"""
    url_del = url_passhport + "targetgroup/del/" + targetgroupname

    try:
        r = requests.get(url_del)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_targetgroup_addtarget(targetname, targetgroupname):
    """Add a target in a targetgroup via API"""
    targetgroup_target_data = {'targetname': targetname, 'targetgroupname': targetgroupname}
    url_addtarget = url_passhport + "targetgroup/addtarget"

    try:
        r = requests.post(url_addtarget, data = targetgroup_target_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_targetgroup_rmtarget(targetname, targetgroupname):
    """Remove a target from a targetgroup via API"""
    targetgroup_target_data = {'targetname': targetname, 'targetgroupname': targetgroupname}
    url_rmtarget = url_passhport + "targetgroup/rmtarget"

    try:
        r = requests.post(url_rmtarget, data = targetgroup_target_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_targetgroup_adduser(email, targetgroupname):
    """Add a user in a targetgroup via API"""
    targetgroup_user_data = {'targetgroupname': targetgroupname, 'email': email}
    url_adduser = url_passhport + "targetgroup/adduser"

    try:
        r = requests.post(url_adduser, data = targetgroup_user_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_targetgroup_rmuser(email, targetgroupname):
    """Remove a user in a targetgroup via API"""
    targetgroup_user_data = {'targetgroupname': targetgroupname, 'email': email}
    url_rmuser = url_passhport + "targetgroup/rmuser"

    try:
        r = requests.post(url_rmuser, data = targetgroup_user_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_targetgroup_addusergroup(usergroupname, targetgroupname):
    """Add a usergroup in a targetgroup via API"""
    targetgroup_usergroup_data = {'targetgroupname': targetgroupname, 'usergroupname': usergroupname}
    url_addusergroup = url_passhport + "targetgroup/addusergroup"

    try:
        r = requests.post(url_addusergroup, data = targetgroup_usergroup_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1
