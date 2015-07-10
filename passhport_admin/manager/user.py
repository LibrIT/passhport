#!/usr/bin/env python
# -*-coding:Utf-8 -*-

from . import python_compat as pyt_compat

def prompt_create():
    """Prompt user to obtain data for request"""
    name = pyt_compat.input_compat("Name: ")
    sshkey = pyt_compat.input_compat("SSH Key: ")
    comment = pyt_compat.input_compat("Comment: ")

    return {"<name>": name, "<sshkey>": sshkey, "<comment>": comment}


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
    name = pyt_compat.input_compat("Name of the user you want to modify: ")

    if req.show("user", {"<name>": name}) == 0:
        new_name = pyt_compat.input_compat("New name: ")
        new_comment = pyt_compat.input_compat("New comment: ")
        new_sshkey = pyt_compat.input_compat("New SSH key: ")

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
