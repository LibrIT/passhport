# -*-coding:Utf-8 -*-

"""Contains functions which make requests to the server for user management"""

import requests

url_passhport = "http://127.0.0.1:5000/"

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
    """Getting data about a user"""

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
