# -*-coding:Utf-8 -*-

"""Contains functions which make requests to the server"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import input

import sys, locale
import requests, re

from . import user as user
from . import target as target
from . import usergroup as usergroup
from . import targetgroup as targetgroup
import config

def ask_confirmation(prompt_confirmation):
    """Same as input() but check if user key in a correct input,
    return True if the user confirms, false otherwise.
    """
    # Hack for the sake of compatibility between 2.7 and 3.4
    sys.stdout.write(prompt_confirmation)
    confirmation = str.upper(input(""))

    # Loop until user types [y/N]
    while confirmation != "Y" and confirmation != "N" and confirmation:
        print("You didn't type 'Y' or 'N', please try again.")
        sys.stdout.write(prompt_confirmation)
        confirmation = str.upper(input(""))

    if confirmation == "Y":
        return True

    return False


def get(url):
    """Send the GET request to the server and print a result"""
    try:
        print(url + " " + config.certificate_path)
        r = requests.get(url, verify=config.certificate_path)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            return 0

    return 1


def list(obj):
    """Get the list of all objects of this type"""
    return get(config.url_passhport + obj + "/list")


def search(obj, param):
    """Get the list of objects matching the pattern"""
    if isinstance(param["<pattern>"], bytes):
        param["<pattern>"] = param["<pattern>"].decode("utf8")

    return get(config.url_passhport + obj + "/search/" + param["<pattern>"])


def show(obj, param):
    """Get data of the given object"""
    if isinstance(param["<name>"], bytes):
        param["<name>"] = param["<name>"].decode("utf8")

    return get(config.url_passhport + obj + "/show/" + param["<name>"])


def delete(obj, param):
    """Deletion on passhportd via API"""
    if isinstance(param["<name>"], bytes):
        param["<name>"] = param["<name>"].decode("utf8")

    if show(obj, {"<name>": param["<name>"]}) == 0:
        if "-f" in param or "--force" in param:
            return get(config.url_passhport + obj + "/delete/" + \
                       param["<name>"])
        else:
            confirmed = ask_confirmation(
                "Are you sure you want to delete " + \
                param["<name>"] + "? [y/N] ")

            if confirmed:
                return get(config.url_passhport + obj + "/delete/" + \
                    param["<name>"])
            else:
                print("Operation aborted.")

    return None


def post(url, data):
    """Send the POST request to the server and print a result"""
    try:
        r = requests.post(url, data = data, verify=config.certificate_path)
    except requests.RequestException as e:
        print("ERROR: " + str(e.message))
    else:
        print(r.text)

        if r.status_code == requests.codes.ok:
            # Copy sshkey on new targets
            if re.findall("\/target\/create", url) and AUTO_DEPLOY_SSHKEY:
                print("Trying to deploy sshkey")
            return 0
        #TODO first connection to a target to deploy a key
        # if url  content target
        # ask_user_if_first_connection
        # connect / prompt pass
        # done => print result.

    return 1


def create(obj, param):
    """Object creation on passhportd via API"""
    objects = {"user": user, "target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    data = getattr(objects[obj], "create")(param)
    url = config.url_passhport + obj + "/create"

    return post(url, data)


def edit(obj, param):
    """Object modification on passhportd via API"""
    objects = {"user": user, "target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    data = getattr(objects[obj], "edit")(param)
    url = config.url_passhport + obj + "/edit"

    return post(url, data)


def adduser(obj, param):
    """Add a user to an object on passhportd via API"""
    objects = {"target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    data = getattr(objects[obj], "adduser")(param)
    url = config.url_passhport + obj + "/adduser"

    return post(url, data)


def rmuser(obj, param):
    """Remove a user from an object on passhportd via API"""
    objects = {"target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    data = getattr(objects[obj], "rmuser")(param)
    url = config.url_passhport + obj + "/rmuser"

    return post(url, data)


def addtarget(obj, param):
    """Add a target to an object on passhportd via API"""
    objects = {"targetgroup": targetgroup}
    data = getattr(objects[obj], "addtarget")(param)
    url = config.url_passhport + obj + "/addtarget"

    return post(url, data)


def rmtarget(obj, param):
    """Remove a target from an object on passhportd via API"""
    objects = {"targetgroup": targetgroup}
    data = getattr(objects[obj], "rmtarget")(param)
    url = config.url_passhport + obj + "/rmtarget"

    return post(url, data)


def addusergroup(obj, param):
    """Add a usergroup to an object on passhportd via API"""
    objects = {"target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    data = getattr(objects[obj], "addusergroup")(param)
    url = config.url_passhport + obj + "/addusergroup"

    return post(url, data)


def rmusergroup(obj, param):
    """Remove a usergroup from an object on passhportd via API"""
    objects = {"target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    data = getattr(objects[obj], "rmusergroup")(param)
    url = config.url_passhport + obj + "/rmusergroup"

    return post(url, data)


def addtargetgroup(obj, param):
    """Add a targetgroup to an object on passhportd via API"""
    objects = {"targetgroup": targetgroup}
    data = getattr(objects[obj], "addtargetgroup")(param)
    url = config.url_passhport + obj + "/addtargetgroup"

    return post(url, data)


def rmtargetgroup(obj, param):
    """Remove a targetgroup from an object on passhportd via API"""
    objects = {"targetgroup": targetgroup}
    data = getattr(objects[obj], "rmtargetgroup")(param)
    url = config.url_passhport + obj + "/rmtargetgroup"

    return post(url, data)
