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
    usergroupname = pyt_compat.input_compat("Usergroupname: ")
    comment       = pyt_compat.input_compat("Comment: ")
    print("")

    return req.requests_usergroup_create(usergroupname, comment)

def prompt_usergroup_show():
    """Ask arguments for showing usergroup"""
    usergroupname = pyt_compat.input_compat("Usergroupname: ")
    print("")

    return req.requests_usergroup_show(usergroupname)

def prompt_usergroup_edit():
    """Ask arguments for editing an existing usergroup"""
    usergroupname = pyt_compat.input_compat("Name of the usergroup you want to modify: ")

    if req.requests_usergroup_show(usergroupname) == 0:
        new_usergroupname = pyt_compat.input_compat("New name: ")
        new_comment       = pyt_compat.input_compat("New comment: ")
        print("")

        return req.requests_usergroup_edit(usergroupname, new_usergroupname, new_comment)

def prompt_usergroup_del():
    """Ask arguments for deleting an existing usergroup"""
    usergroupname = pyt_compat.input_compat("Usergroupname: ")
    print("")

    return req.requests_usergroup_del(usergroupname)

def prompt_usergroup_adduser(email, usergroupname):
    """Add a user to a usergroup"""
    return req.requests_usergroup_adduser(email, usergroupname)

def prompt_usergroup_rmuser(email, usergroupname):
    """Remove a user from a usergroup"""
    return req.requests_usergroup_rmuser(email, usergroupname)

def prompt_usergroup_addusergroup(subusergroupname, usergroupname):
    """Add a usergroup (subusergroup) to a usergroup"""
    return req.requests_usergroup_addusergroup(subusergroupname, usergroupname)
