# -*-coding:Utf-8 -*-

"""Contains functions that interpret commmands from the CLI and
call request functions
"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import input

from . import requests_functions as req

from . import user as user
from . import target as target
from . import usergroup as usergroup
from . import targetgroup as targetgroup

def list(obj):
    """List all object of this type"""
    return req.list(obj)


def search(obj):
    """Search an object of this type which match the pattern"""
    pattern = input("Pattern: ")
    return req.search(obj, {"<pattern>": pattern})


def show(obj):
    """Ask arguments for showing the object"""
    name = input("Name: ")
    return req.show(obj, {"<name>": name})


def delete(obj):
    """Ask arguments for deleting an existing object"""
    name = input("Name: ")

    if req.show(obj, {"<name>": name}) == 0:
        confirmed = req.ask_confirmation("Are you sure you want to delete " + \
            name + "? [y/N] ")

        if confirmed:
            return req.get(req.url_passhport + obj + "/delete/" + name)
        else:
            print("Operation aborted.")

    return None


def create(obj):
    """Ask arguments for object creation"""
    objects = {"user": user, "target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    data = getattr(objects[obj], "prompt_create")()

    return req.create(obj, data)


def edit(obj):
    """Ask arguments for editing an existing object"""
    objects = {"user": user, "target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    # We send the module requests_functions as an object
    # to the function prompt_edit to avoid circular import.
    # prompt_edit() needs the function req.show() to check
    # if the object to edit does exist.
    data = getattr(objects[obj], "prompt_edit")(req)

    if data:
        return req.edit(obj, data)

    return None


def adduser(obj):
    """Ask arguments for adding a user to an object"""
    objects = {"target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    data = getattr(objects[obj], "prompt_adduser")()

    if data:
        return req.adduser(obj, data)

    return None

def rmuser(obj):
    """Ask arguments for removing a user from an object"""
    objects = {"target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    data = getattr(objects[obj], "prompt_rmuser")()

    if data:
        return req.rmuser(obj, data)

    return None

def addtarget(obj):
    """Ask arguments for adding a target to an object"""
    objects = {"targetgroup": targetgroup}
    data = getattr(objects[obj], "prompt_addtarget")()

    if data:
        return req.addtarget(obj, data)

    return None

def rmtarget(obj):
    """Ask arguments for removing a target from an object"""
    objects = {"targetgroup": targetgroup}
    data = getattr(objects[obj], "prompt_rmtarget")()

    if data:
        return req.rmtarget(obj, data)

    return None

def addusergroup(obj):
    """Ask arguments for adding a usergroup to an object"""
    objects = {"target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    data = getattr(objects[obj], "prompt_addusergroup")()

    if data:
        return req.addusergroup(obj, data)

    return None

def rmusergroup(obj):
    """Ask arguments for removing a usergroup from an object"""
    objects = {"target": target, "usergroup": usergroup,
            "targetgroup": targetgroup}
    data = getattr(objects[obj], "prompt_rmusergroup")()

    if data:
        return req.rmusergroup(obj, data)

    return None

def addtargetgroup(obj):
    """Ask arguments for adding a targetgroup to an object"""
    objects = {"targetgroup": targetgroup}
    data = getattr(objects[obj], "prompt_addtargetgroup")()

    if data:
        return req.addtargetgroup(obj, data)

    return None

def rmtargetgroup(obj):
    """Ask arguments for removing a targetgroup from an object"""
    objects = {"targetgroup": targetgroup}
    data = getattr(objects[obj], "prompt_rmtargetgroup")()

    if data:
        return req.rmtargetgroup(obj, data)

    return None
