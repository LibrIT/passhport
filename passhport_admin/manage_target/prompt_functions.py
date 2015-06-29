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
    targetname = pyt_compat.input_compat("Targetname: ")
    hostname = pyt_compat.input_compat("Hostname: ")
    comment = pyt_compat.input_compat("Comment: ")
    sshoptions = pyt_compat.input_compat("SSH options: ")

    port_is_int = False
    while not port_is_int:  # Loop to key in port number correctly
        port = pyt_compat.input_compat("Port: ")

        # We assume the port is an int, we will check right after
        port_is_int = True

        # Verifying that the port is actually an int
        try:
            port = int(port)
        except ValueError:
            print("You didn’t key in a port number. Please try again.")
            port_is_int = False

    servertype = pyt_compat.input_compat("Server’s type: ")
    autocommand = pyt_compat.input_compat("Autocommand: ")
    print("")

    return req.requests_target_create(
        targetname,
        hostname,
        comment,
        sshoptions,
        port,
        servertype,
        autocommand)


def prompt_target_show():
    """Ask arguments for showing target"""
    targetname = pyt_compat.input_compat("Targetname: ")
    print("")

    return req.requests_target_show(targetname)


def prompt_target_edit():
    """Ask arguments for editing an existing target"""
    targetname = pyt_compat.input_compat(
        "Name of the target you want to modify: ")

    if req.requests_target_show(targetname) == 0:
        new_targetname = pyt_compat.input_compat("New targetname: ")
        new_hostname = pyt_compat.input_compat("New hostname: ")
        new_comment = pyt_compat.input_compat("New comment: ")
        new_sshoptions = pyt_compat.input_compat("New SSH options: ")

        port_is_int = False
        while not port_is_int:  # Loop to key in port number correctly
            new_port = pyt_compat.input_compat("Port: ")

            # We assume the port is an int, we will check right after
            port_is_int = True

            # Verifying that the port is actually an int
            try:
                new_port = int(new_port)
            except ValueError:
                print("You didn’t key in a port number. Please try again.")
                port_is_int = False

        new_servertype = pyt_compat.input_compat("New server’s type: ")
        new_autocommand = pyt_compat.input_compat("New autocommand: ")
        print("")

        return req.requests_target_edit(
            targetname,
            new_targetname,
            new_hostname,
            new_comment,
            new_sshoptions,
            new_port,
            new_servertype,
            new_autocommand)

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


def prompt_target_addusergroup(usergroupname, targetname):
    """Add a usergroup to a target"""
    return req.requests_target_addusergroup(usergroupname, targetname)


def prompt_target_rmusergroup(usergroupname, targetname):
    """Remove a usergroup from a target"""
    return req.requests_target_rmusergroup(usergroupname, targetname)
