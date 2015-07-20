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
    return req.delete({"<name>": name})


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
    data = getattr(objects[obj], "prompt_edit")()

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
