# -*-coding:Utf-8 -*-

"""Contains functions which make requests to the server for user's management"""

import requests

url_passhport = "http://127.0.0.1:5000/"


def list():
    """Get the list of all users"""
    url_list = url_passhport + "user/list"

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
    """Get the list of users following the pattern"""
    url_search = url_passhport + "user/search/" + param['<pattern>']

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
    """User creation on passhportd via API"""
    email = param['<email>']
    sshkey = param['<sshkey>']
    comment = ""
    if '<comment>' in param:
        comment = param['<comment>']
    user_data = {'email': email, 'comment': comment, 'sshkey': sshkey}
    url_create = url_passhport + "user/create"

    try:
        r = requests.post(url_create, data=user_data)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def show(param):
    """Get data about a user"""
    url_show = url_passhport + "user/show/" + param['<email>']

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
    """User modification on passhportd via API"""
    email = param['<email>']
    new_email = ""
    new_comment = ""
    new_sshkey = ""
    if '--newemail' in param:
        new_email = param['--newemail']
    if '--newcomment' in param:
        new_comment = param['--newcomment']
    if '--newsshkey' in param:
        new_sshkey = param['--newsshkey']
    user_data = {
        'email': email,
        'new_email': new_email,
        'new_comment': new_comment,
        'new_sshkey': new_sshkey}
    url_edit = url_passhport + "user/edit"

    try:
        r = requests.post(url_edit, data=user_data)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def delete(param):
    """User deletion on passhportd via API"""
    url_del = url_passhport + "user/del/" + param['<email>']

    try:
        r = requests.get(url_del)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1
