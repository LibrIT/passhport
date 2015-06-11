# -*-coding:Utf-8 -*-

"""Contains functions to interpret commmands from the cli"""

import requests_functions as req

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
