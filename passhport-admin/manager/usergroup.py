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

    return {"<name>": name, "--comment": comment}


def create(param):
    """Format param for usergroup creation"""
    comment = ""

    if "--comment" in param:
        comment = param["--comment"]

    return {"name": param["<name>"],
            "comment": comment}


def prompt_edit(req):
    """Prompt usergroup to obtain data to request"""
    name = input("Name of the usergroup you want to modify: ")

    if req.show("usergroup", {"<name>": name}) == 0:
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
    """Format param for usergroup edition"""
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
    usergroupname = input("Usergroupname: ")

    return {"<username>": username,
            "<usergroupname>": usergroupname}


def adduser(param):
    """Format param to add a user"""
    return {"username": param["<username>"],
            "usergroupname": param["<usergroupname>"]}


def prompt_rmuser():
    """Prompt user to obtain data to remove a user"""
    username = input("Username: ")
    usergroupname = input("Usergroupname: ")

    return {"<username>": username,
            "<usergroupname>": usergroupname}


def rmuser(param):
    """Format param to remove a user"""
    return {"username": param["<username>"],
            "usergroupname": param["<usergroupname>"]}


def prompt_addusergroup():
    """Prompt user to obtain data to add a usergroup"""
    subusergroupname = input("Subusergroupname: ")
    usergroupname = input("Usergroupname: ")

    return {"<subusergroupname>": subusergroupname,
            "<usergroupname>": usergroupname}


def addusergroup(param):
    """Format param to add a usergroup"""
    return {"subusergroupname": param["<subusergroupname>"],
            "usergroupname": param["<usergroupname>"]}


def prompt_rmusergroup():
    """Prompt user to obtain data to remove a usergroup"""
    subusergroupname = input("Subsergroupname: ")
    usergroupname = input("Usergroupname: ")

    return {"<subusergroupname>": subusergroupname,
            "<usergroupname>": usergroupname}


def rmusergroup(param):
    """Format param to remove a usergroup"""
    return {"subusergroupname": param["<subusergroupname>"],
            "usergroupname": param["<usergroupname>"]}
