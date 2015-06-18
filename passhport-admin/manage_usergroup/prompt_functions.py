# -*-coding:Utf-8 -*-

"""Contains functions that interpret commmands from the CLI and call request functions for usergroup's management"""

import python_compat as pyt_compat
import requests_functions as req

def prompt_usergroup_list():
    """List all usergroups in the database"""
    return req.requests_usergroup_list()

def prompt_usergroup_search(pattern):
    """Search a usergroup according to the pattern"""
    return req.requests_usergroup_search(pattern)

def prompt_usergroup_create():
    """Ask arguments for usergroup creation"""
    groupname = pyt_compat.input_compat("Groupname: ")
    comment   = pyt_compat.input_compat("Comment: ")
    print("")

    return req.requests_usergroup_create(groupname, comment)

def prompt_usergroup_show():
    """Ask arguments for showing usergroup"""
    groupname = pyt_compat.input_compat("Groupname: ")
    print("")

    return req.requests_usergroup_show(groupname)

def prompt_usergroup_edit():
    """Ask arguments for editing an existing usergroup"""
    groupname = pyt_compat.input_compat("Name of the usergroup you want to modify: ")

    if req.requests_usergroup_show(groupname) == 0:
        new_groupname = pyt_compat.input_compat("New name: ")
        new_comment = pyt_compat.input_compat("New comment: ")
        print("")

        return req.requests_usergroup_edit(groupname, new_groupname, new_comment)

def prompt_usergroup_del():
    """Ask arguments for deleting an existing usergroup"""
    groupname = pyt_compat.input_compat("Groupname: ")
    print("")

    return req.requests_usergroup_del(groupname)
