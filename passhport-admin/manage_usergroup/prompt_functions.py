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
    email   = pyt_compat.input_compat("Email: ")
    comment = pyt_compat.input_compat("Comment: ")
    sshkey  = pyt_compat.input_compat("SSHKey: ")
    print("")

    return req.requests_usergroup_create(email, comment, sshkey)

def prompt_usergroup_show():
    """Ask arguments for showing usergroup"""
    email = pyt_compat.input_compat("Email: ")
    print("")

    return req.requests_usergroup_show(email)

def prompt_usergroup_edit():
    """Ask arguments for editing an existing usergroup"""
    email = pyt_compat.input_compat("Email of the usergroup you want to modify: ")

    if req.requests_usergroup_show(email) == 0:
        new_email   = pyt_compat.input_compat("New email: ")
        new_comment = pyt_compat.input_compat("New comment: ")
        new_sshkey  = pyt_compat.input_compat("New SSH key: ")
        print("")

        return req.requests_usergroup_edit(email, new_email, new_comment, new_sshkey)

def prompt_usergroup_del():
    """Ask arguments for deleting an existing usergroup"""
    email = pyt_compat.input_compat("Email: ")
    print("")

    return req.requests_usergroup_del(email)
