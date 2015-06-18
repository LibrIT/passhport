# -*-coding:Utf-8 -*-

"""Contains functions that interpret commmands from the CLI and call request functions for target's management"""

import python_compat as pyt_compat
import requests_functions as req

def prompt_target_list():
    """List all targets in the database"""
    return req.requests_target_list()

def prompt_target_search(pattern):
    """Search a target according to the pattern"""
    return req.requests_target_search(pattern)

def prompt_target_create():
    """Ask arguments for target creation"""
    targetname  = pyt_compat.input_compat("Targetname: ")
    hostname    = pyt_compat.input_compat("Hostname: ")
    comment     = pyt_compat.input_compat("Comment: ")
    sshoptions  = pyt_compat.input_compat("SSH options: ")
    port        = pyt_compat.input_compat("Port: ")
    servertype  = pyt_compat.input_compat("Server’s type: ")
    autocommand = pyt_compat.input_compat("Autocommand: ")
    print("")

    return req.requests_target_create(targetname, hostname, comment, sshoptions, port, servertype, autocommand)

def prompt_target_show():
    """Ask arguments for showing target"""
    targetname = pyt_compat.input_compat("Targetname: ")
    print("")

    return req.requests_target_show(targetname)

def prompt_target_show_users():
    """Ask arguments for showing target and its user list"""
    targetname = pyt_compat.input_compat("Targetname: ")
    print("")

    return req.requests_target_show_users(targetname)

def prompt_target_show_usergroups():
    """Ask arguments for showing target and its usergroup list"""
    targetname = pyt_compat.input_compat("Targetname: ")
    print("")

    return req.requests_target_show_usergroups(targetname)

def prompt_target_edit():
    """Ask arguments for editing an existing target"""
    targetname = pyt_compat.input_compat("Name of the target you want to modify: ")

    if req.requests_target_show(targetname) == 0:
        new_targetname  = pyt_compat.input_compat("New targetname: ")
        new_hostname    = pyt_compat.input_compat("New hostname: ")
        new_comment     = pyt_compat.input_compat("New comment: ")
        new_sshoptions  = pyt_compat.input_compat("New SSH options: ")
        new_port        = pyt_compat.input_compat("New port: ")
        new_servertype  = pyt_compat.input_compat("New server’s type: ")
        new_autocommand = pyt_compat.input_compat("New autocommand: ")
        print("")

        return req.requests_target_edit(targetname, new_targetname, new_hostname, new_comment, new_sshoptions, new_port, new_servertype, new_autocommand)

    return None

def prompt_target_del():
    """Ask arguments for deleting an existing target"""
    targetname = pyt_compat.input_compat("Targetname: ")
    print("")

    return req.requests_target_del(targetname)

def prompt_target_adduser(email, targetname):
    """Add a user to a target"""
    return req.requests_target_adduser(email, targetname)

def prompt_target_rmuser(email, targetname):
    """Remove a user from a target"""
    return req.requests_target_rmuser(email, targetname)
