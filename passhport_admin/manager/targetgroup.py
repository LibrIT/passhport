#!/usr/bin/env python
# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import input


def prompt_create():
    """Prompt user to obtain data for request"""
    name = input("Name: ")
    comment = input("Comment: ")

    return {"<name>": name, "<comment>": comment}


def create(param):
    """Format param for targetgroup creation"""
    comment = ""

    if "--comment" in param:
        comment = param["--comment"]

    return {"name": param["<name>"],
            "comment": comment}


def prompt_edit(req):
    """Prompt targetgroup to obtain data to request"""
    name = input("Name of the targetgroup you want to modify: ")

    if req.show("targetgroup", {"<name>": name}) == 0:
        new_name = input("New name: ")
        new_comment = input("New comment: ")
        if len(new_comment.strip()) == 0:
            answer = input("Remove original comment? [y/N]")
            if answer == "y":
                new_comment = "PASSHPORTREMOVECOMMENT"

        return {"<name>": name,
                "--newname": new_name,
                "--newcomment": new_comment}

    return None


def edit(param):
    """Format param for targetgroup edition"""
    new_name = ""
    new_comment = ""

    if "--newname" in param:
        new_name = param["--newname"]

    if "--newcomment" in param:
        new_comment = param["--newcomment"]

    return {"name": param["<name>"],
            "new_name": new_name,
            "new_comment": new_comment}

def prompt_adduser():
    """Prompt user to obtain data to add a user"""
    username = input("Username: ")
    targetgroupname = input("Targetgroupname: ")

    return {"<username>": username,
            "<targetgroupname>": targetgroupname}


def adduser(param):
    """Format param to add a user"""
    return {"username": param["<username>"],
            "targetgroupname": param["<targetgroupname>"]}


def prompt_rmuser():
    """Prompt user to obtain data to remove a user"""
    username = input("Username: ")
    targetgroupname = input("Targetgroupname: ")

    return {"<username>": username,
            "<targetgroupname>": targetgroupname}


def rmuser(param):
    """Format param to remove a user"""
    return {"username": param["<username>"],
            "targetgroupname": param["<targetgroupname>"]}


def prompt_addtarget():
    """Prompt user to obtain data to add a target"""
    targetname = input("Targetname: ")
    targetgroupname = input("Targetgroupname: ")

    return {"<targetname>": targetname,
            "<targetgroupname>": targetgroupname}


def addtarget(param):
    """Format param to add a target"""
    return {"targetname": param["<targetname>"],
            "targetgroupname": param["<targetgroupname>"]}


def prompt_rmtarget():
    """Prompt user to obtain data to remove a target"""
    targetname = input("Targetname: ")
    targetgroupname = input("Targetgroupname: ")

    return {"<targetname>": targetname,
            "<targetgroupname>": targetgroupname}


def rmtarget(param):
    """Format param to remove a target"""
    return {"targetname": param["<targetname>"],
            "targetgroupname": param["<targetgroupname>"]}


def prompt_addusergroup():
    """Prompt user to obtain data to add a usergroup"""
    usergroupname = input("Usergroupname: ")
    targetgroupname = input("Targetgroupname: ")

    return {"<usergroupname>": usergroupname,
            "<targetgroupname>": targetgroupname}


def addusergroup(param):
    """Format param to add a usergroup"""
    return {"usergroupname": param["<usergroupname>"],
            "targetgroupname": param["<targetgroupname>"]}


def prompt_rmusergroup():
    """Prompt user to obtain data to remove a usergroup"""
    usergroupname = input("Usergroupname: ")
    targetgroupname = input("Targetgroupname: ")

    return {"<usergroupname>": usergroupname,
            "<targetgroupname>": targetgroupname}


def rmusergroup(param):
    """Format param to remove a usergroup"""
    return {"usergroupname": param["<usergroupname>"],
            "targetgroupname": param["<targetgroupname>"]}


def prompt_addtargetgroup():
    """Prompt user to obtain data to add a targetgroup"""
    subtargetgroupname = input("Subtargetgroupname: ")
    targetgroupname = input("Targetgroupname: ")

    return {"<subtargetgroupname>": subtargetgroupname,
            "<targetgroupname>": targetgroupname}


def addtargetgroup(param):
    """Format param to add a targetgroup"""
    return {"subtargetgroupname": param["<subtargetgroupname>"],
            "targetgroupname": param["<targetgroupname>"]}


def prompt_rmtargetgroup():
    """Prompt user to obtain data to remove a targetgroup"""
    subtargetgroupname = input("Subtargetgroupname: ")
    targetgroupname = input("Targetgroupname: ")

    return {"<subtargetgroupname>": subtargetgroupname,
            "<targetgroupname>": targetgroupname}


def rmtargetgroup(param):
    """Format param to remove a targetgroup"""
    return {"subtargetgroupname": param["<subtargetgroupname>"],
            "targetgroupname": param["<targetgroupname>"]}
