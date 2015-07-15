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


def prompt_edit():
    """Prompt targetgroup to obtain data to request"""
    name = input("Name of the targetgroup you want to modify: ")

    if req.show("targetgroup", {"<name>": name}) == 0:
        new_name = input("New name: ")
        new_comment = input("New comment: ")

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
