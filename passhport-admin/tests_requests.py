#!/usr/bin/env python
# -*-coding:Utf-8 -*-

import requests

url_passhport = "http://127.0.0.1:5000/"

def create_user():
    """Create a user"""

    print("Creating_user…")

    user_data = {'username': 'efrit', 'email': 'awesome_mail@onemail.org', 'comment': 'Utilisateur de test', 'sshkey': 'this_is_an_awesome_private_key_example'}
    url_create = url_passhport + "user/create"

    try:
        r = requests.post(url_create, data = user_data)
    except ConnectionError, e:
        print("ERROR:" + e.message)
    except HTTPError, e:
        print("ERROR:" + e.message)
    except Timeout, e:
        print("ERROR:" + e.message)
    except TooManyRedirects, e:
        print("ERROR:" + e.message)

    print(r.text)

    if r.status_code == requests.codes.ok:
        return 0

    return 1

def search_user():
    """Search a user"""

    print("Searching user…")

    username = "efrit"
    url_search = url_passhport + "user/search/" + username

    try:
        r = requests.get(url_search)
    except ConnectionError, e:
        print("ERROR:" + e.message)
    except HTTPError, e:
        print("ERROR:" + e.message)
    except Timeout, e:
        print("ERROR:" + e.message)
    except TooManyRedirects, e:
        print("ERROR:" + e.message)

    print(r.text)

    if r.status_code == requests.codes.ok:
        return 0

    return 1

def list_users():
    """List users"""

    print("Listing users…")

    url_list = url_passhport + "user/list"

    try:
        r = requests.get(url_list)
    except ConnectionError, e:
        print("ERROR:" + e.message)
    except HTTPError, e:
        print("ERROR:" + e.message)
    except Timeout, e:
        print("ERROR:" + e.message)
    except TooManyRedirects, e:
        print("ERROR:" + e.message)

    print(r.text)

    if r.status_code == requests.codes.ok:
        return 0

    return 1

def show_user():
    """Show a user"""

    print("Showing user…")

    username = "efrit"
    url_show = url_passhport + "user/show/" + username

    try:
        r = requests.get(url_show)
    except ConnectionError, e:
        print("ERROR:" + e.message)
    except HTTPError, e:
        print("ERROR:" + e.message)
    except Timeout, e:
        print("ERROR:" + e.message)
    except TooManyRedirects, e:
        print("ERROR:" + e.message)

    print(r.text)

    if r.status_code == requests.codes.ok:
        return 0

    return 1

def modify_user():
    """Modify a user"""

    print("Modifying user…")

    url_modify = url_passhport + "user/edit"
    user_data = {'username': 'efrit', 'newusername': 'newefrit', 'email': 'somerandom@email.org', 'comment': 'acomment', 'sshkey': 'a_random_key'}

    try:
        r = requests.post(url_modify, data = user_data)
    except ConnectionError, e:
        print("ERROR:" + e.message)
    except HTTPError, e:
        print("ERROR:" + e.message)
    except Timeout, e:
        print("ERROR:" + e.message)
    except TooManyRedirects, e:
        print("ERROR:" + e.message)

    print(r.text)

    if r.status_code == requests.codes.ok:
        return 0

    return 1

def create_target():
    """Create a target"""

    print("Creating target…")

    target_data = {'targetname': 'dat_server', 'hostname': '127.0.01', 'comment': 'test target', 'sshoptions': '-z', 'port': '22', 'servertype': 'Debian', 'autocommand': 'dat_bash_command'}
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

create_target()
