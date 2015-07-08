# -*-coding:Utf-8 -*-

"""Contains functions that interpret commmands from the CLI and call request functions for target's management"""

import python_compat as pyt_compat
import requests_functions as req


def list():
    """List all targets in the database"""
    return req.list()


def search(pattern):
    """Search a target according to the pattern"""
    return req.search({'<pattern>': pattern})


def create():
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

    return req.create({'<targetname>': targetname,
        '<hostname>': hostname,
        '<comment>': comment,
        '<sshoptions>': sshoptions,
        '<port>': port,
        '<servertype>': servertype,
        '<autocommand>': autocommand})


def show():
    """Ask arguments for showing target"""
    targetname = pyt_compat.input_compat("Targetname: ")

    return req.show({'<targetname': targetname})


def edit():
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

        return req.create({'<targetname>': targetname,
            '<hostname>': new_hostname,
            '<comment>': new_comment,
            '<sshoptions>': new_sshoptions,
            '<port>': new_port,
            '<servertype>': new_servertype,
            '<autocommand>': new_autocommand})


def delet():
    """Ask arguments for deleting an existing target"""
    targetname = pyt_compat.input_compat("Targetname: ")

    return req.delete({'<targetname>': targetname})


def adduser():
    """Add a user to a target"""
    #TODO ask for email/target
    return req.adduser({'<email>': email, '<targetname>': targetname})


def rmuser():
    """Remove a user from a target"""
    #TODO ask for email/target
    return req.rmuser({'<email>': email, '<targetname>': targetname})


def addusergroup():
    """Add a usergroup to a target"""
    #TODO ask for usergroup/target
    return req.addusergroup({'<usergroupname>': usergroupname, 
        '<targetname>': targetname})


def rmusergroup():
    """Remove a usergroup from a target"""
    #TODO ask for usergroup/target
    return req.rmusergroup(usergroupname, targetname)
