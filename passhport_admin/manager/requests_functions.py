# -*-coding:Utf-8 -*-

"""Contains functions which make requests to the server"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import requests

from . import user as user
from . import target as target
from . import usergroup as usergroup
from . import targetgroup as targetgroup

url_passhport = "http://127.0.0.1:5000/"


def get(url):
    """Send the GET request to the server and print a result"""
    try:
        r = requests.get(url)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def list(obj):
    """Get the list of all objects of this type"""
    return get(url_passhport + obj + "/list")


def search(obj, param):
    """Get the list of objects matching the pattern"""
    return get(url_passhport + obj + "/search/" + param["<pattern>"])


def show(obj, param):
    """Get data of the given object"""
    return get(url_passhport + obj + "/show/" + param["<name>"])


def delete(obj, param):
    """Deletion on passhportd via API"""
    return get(url_passhport + obj + "/delete/" + param["<name>"])


def post(url, data):
    """Send the POST request to the server and print a result"""
    try:
        r = requests.post(url, data = data)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def create(obj, param):
    """Object creation on passhportd via API"""
    objects = {"user": user, "target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    data = getattr(objects[obj], "create")(param)
    url = url_passhport + obj + "/create"

    return post(url, data)


def edit(obj, param):
    """Object modification on passhportd via API"""
    objects = {"user": user, "target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    data = getattr(objects[obj], "edit")(param)
    url = url_passhport + obj + "/edit"

    return post(url, data)
