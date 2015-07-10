# -*-coding:Utf-8 -*-

"""Contains functions that interpret commmands from the CLI and
call request functions
"""

from . import python_compat as pyt_compat
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
    pattern = pyt_compat.input_compat("Pattern: ")

    return req.search(obj, {"<pattern>": pattern})


def show(obj):
    """Ask arguments for showing the object"""
    name = pyt_compat.input_compat("Name: ")

    return req.show(obj, {"<name>": name})


def delete(obj):
    """Ask arguments for deleting an existing user"""
    name = pyt_compat.input_compat("Name: ")

    return req.delete({"<name>": name})


def create(obj):
    """Ask arguments for user creation"""
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
