# -*-coding:Utf-8 -*-

"""Contains functions that interpret commmands from the CLI and call request functions for target’s management"""

import requests_functions as req

def prompt_target_list():
    """List all targets in the database"""

    return req.requests_target_list()

def prompt_target_search(pattern):
    """Search a target according to the pattern"""

    return req.requests_target_search(pattern)

def prompt_target_create():
    """Ask arguments for target creation"""

    # 2.7 compatibility
    try: input = raw_input
    except NameError: pass

    targetname  = input("Targetname: ")
    hostname    = input("Hostname: ")
    comment     = input("Comment: ")
    sshoptions  = input("SSH options: ")
    port        = input("Port: ")
    servertype  = input("Server’s type: ")
    autocommand = input("Autocommand: ")
    print("")

    return req.requests_target_create(targetname, hostname, comment, sshoptions, port, servertype, autocommand)

def prompt_target_show():
    """Ask arguments for showing target"""

    # 2.7 compatibility
    try: input = raw_input
    except NameError: pass

    targetname = input("Targetname: ")
    print("")

    return req.requests_target_show(targetname)

def prompt_target_edit():
    """Ask arguments for editing an existing target"""

    # 2.7 compatibility
    try: input = raw_input
    except NameError: pass

    targetname = input("Name of the target you want to modify: ")

    if req.requests_target_show(targetname) == 0:
        new_targetname  = input("New targetname: ")
        new_hostname    = input("New hostname: ")
        new_comment     = input("New comment: ")
        new_sshoptions  = input("New SSH options: ")
        new_port        = input("New port: ")
        new_servertype  = input("New server’s type: ")
        new_autocommand = input("New autocommand: ")
        print("")

        return req.requests_target_edit(targetname, new_targetname, new_hostname, new_comment, new_sshoptions, new_port, new_servertype, new_autocommand)

    return None

def prompt_target_del():
    """Ask arguments for deleting an existing target"""

    # 2.7 compatibility
    try: input = raw_input
    except NameError: pass

    targetname = input("Targetname: ")
    print("")

    return req.requests_target_del(targetname)

def prompt_target_adduser(email, targetname):
    """Add a user to a target"""

    return req.requests_target_adduser(email, targetname)
