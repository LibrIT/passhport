#!/usr/bin/env python
# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import input

def prompt_create():
    """Prompt user to obtain data for request"""
    name = input("Name: ")
    sshkey = input("SSH Key: ")
    comment = input("Comment: ")

    return {"<name>": name, "<sshkey>": sshkey, "--comment": comment}


def create(param):
    """Format param for user creation"""
    comment = ""

    if "--comment" in param:
        comment = param["--comment"]

    return {"name": param["<name>"],
            "sshkey": param["<sshkey>"],
            "comment": comment}


def prompt_edit():
    """Prompt user to obtain data to request"""
    name = input("Name of the user you want to modify: ")

    if req.show("user", {"<name>": name}) == 0:
        new_name = input("New name: ")
        new_comment = input("New comment: ")
        new_sshkey = input("New SSH key: ")

        return {"<name>": name,
                "--newname": new_name,
                "--newcomment": new_comment,
                "--newsshkey": new_sshkey}

    return None

def edit(param):
    """Format param for user edition"""
    new_name = ""
    new_comment = ""
    new_sshkey = ""

    if "--newname" in param:
        new_name = param["--newname"]
    if "--newcomment" in param:
        new_comment = param["--newcomment"]
    if "--newsshkey" in param:
        new_sshkey = param["--newsshkey"]

    return {"name": param["<name>"],
            "new_name": new_name,
            "new_comment": new_comment,
            "new_sshkey": new_sshkey}
