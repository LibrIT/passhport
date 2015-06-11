# -*-coding:Utf-8 -*-

"""Contains functions to interpret commmands from the cli"""

import requests_functions as req

def prompt_user_list():
    """List all users in the database"""

    return req.requests_user_list()

def prompt_user_search(pattern):
    """Search a user according to the pattern"""

    return req.requests_user_search(pattern)

def prompt_user_create():
    """Ask arguments for user creation"""

    # 2.7 compatibility
    try: input = raw_input
    except NameError: pass

    email = input("Email: ")
    comment = input("Comment: ")
    sshkey = input("SSHKey: ")
    print("")

    return req.requests_user_create(email, comment, sshkey)

def prompt_user_show():
    """Ask arguments for showing"""

    # 2.7 compatibility
    try: input = raw_input
    except NameError: pass

    email = input("Email: ")
    print("")

    return req.requests_user_show(email)
