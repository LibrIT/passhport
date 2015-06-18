# -*-coding:Utf-8 -*-

"""Contains functions that interpret commmands from the CLI and call request functions for user's management"""

import python_compat as pyt_compat
import requests_functions as req

def prompt_user_list():
    """List all users in the database"""
    return req.requests_user_list()

def prompt_user_search(pattern):
    """Search a user according to the pattern"""
    return req.requests_user_search(pattern)

def prompt_user_create():
    """Ask arguments for user creation"""
    email   = pyt_compat.input_compat("Email: ")
    comment = pyt_compat.input_compat("Comment: ")
    sshkey  = pyt_compat.input_compat("SSHKey: ")
    print("")

    return req.requests_user_create(email, comment, sshkey)

def prompt_user_show():
    """Ask arguments for showing user"""
    email = pyt_compat.input_compat("Email: ")
    print("")

    return req.requests_user_show(email)

def prompt_user_edit():
    """Ask arguments for editing an existing user"""
    email = pyt_compat.input_compat("Email of the user you want to modify: ")

    if req.requests_user_show(email) == 0:
        new_email   = pyt_compat.input_compat("New email: ")
        new_comment = pyt_compat.input_compat("New comment: ")
        new_sshkey  = pyt_compat.input_compat("New SSH key: ")
        print("")

        return req.requests_user_edit(email, new_email, new_comment, new_sshkey)

def prompt_user_del():
    """Ask arguments for deleting an existing user"""
    email = pyt_compat.input_compat("Email: ")
    print("")

    return req.requests_user_del(email)
