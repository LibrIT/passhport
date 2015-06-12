# -*-coding:Utf-8 -*-

"""Contains functions which make requests to the server for user management"""

import requests

url_passhport = "http://127.0.0.1:5000/"

##### User #####
def requests_user_list():
    """Get the list of all users"""

    url_list = url_passhport + "user/list"

    try:
        r = requests.get(url_list)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_user_search(pattern):
    """Get the list of users following the pattern"""

    url_search = url_passhport + "user/search/" + pattern

    try:
        r = requests.get(url_search)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_user_create(email, comment, sshkey):
    """User creation on passhportd via API"""

    user_data = {'email': email, 'comment': comment, 'sshkey': sshkey}
    url_create = url_passhport + "user/create"

    try:
        r = requests.post(url_create, data = user_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_user_show(email):
    """Get data about a user"""

    url_show = url_passhport + "user/show/" + email

    try:
        r = requests.get(url_show)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_user_edit(email, new_email, new_comment, new_sshkey):
    """User modification on passhportd via API"""

    user_data = {'email': email, 'new_email': new_email, 'new_comment': new_comment, 'new_sshkey': new_sshkey}
    url_edit = url_passhport + "user/edit"

    try:
        r = requests.post(url_edit, data = user_data)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

def requests_user_del(email):
    """User deletion on passhportd via API"""

    url_del = url_passhport + "user/del/" + email

    try:
        r = requests.get(url_del)
    except requests.RequestException, e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1

##### Target #####
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

def requests_target_edit(targetname, new_targetname, new_hostname, new_comment, new_sshoptions, new_port, new_servertype, new_autocommand):
    """Target modification on passhportd via API"""

    target_data = {'targetname': targetname, 'new_targetname': new_targetname, 'new_hostname': new_hostname, 'new_comment': new_comment, 'new_sshoptions': new_sshoptions, 'new_port': new_port, 'new_servertype': new_servertype, 'new_autocommand': new_autocommand}
    url_edit = url_passhport + "target/edit/"

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
