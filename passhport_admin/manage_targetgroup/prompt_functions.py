# -*-coding:Utf-8 -*-

"""Contains functions that interpret commmands from the CLI and call request functions for targetgroup's management"""

import python_compat as pyt_compat
import requests_functions as req

def prompt_targetgroup_list():
    """List all targetgroups in the database"""
    return req.requests_targetgroup_list()

def prompt_targetgroup_search(pattern):
    """Search a targetgroup according to the pattern"""
    return req.requests_targetgroup_search(pattern)

def prompt_targetgroup_create():
    """Ask arguments for targetgroup creation"""
    targetgroupname = pyt_compat.input_compat("Targetgroupname: ")
    comment         = pyt_compat.input_compat("Comment: ")
    print("")

    return req.requests_targetgroup_create(targetgroupname, comment)

def prompt_targetgroup_show():
    """Ask arguments for showing targetgroup"""
    targetgroupname = pyt_compat.input_compat("Targetgroupname: ")
    print("")

    return req.requests_targetgroup_show(targetgroupname)

def prompt_targetgroup_show_targets():
    """Ask arguments for showing target list of the targetgroup"""
    targetgroupname = pyt_compat.input_compat("Targetgroupname: ")
    print("")

    return req.requests_targetgroup_show_targets(targetgroupname)

def prompt_targetgroup_edit():
    """Ask arguments for editing an existing targetgroup"""
    targetgroupname = pyt_compat.input_compat("Name of the targetgroup you want to modify: ")

    if req.requests_targetgroup_show(targetgroupname) == 0:
        new_targetgroupname = pyt_compat.input_compat("New targetgroupname: ")
        new_comment         = pyt_compat.input_compat("New comment: ")
        print("")

        return req.requests_targetgroup_edit(targetgroupname, new_targetgroupname, new_comment)

    return None

def prompt_targetgroup_del():
    """Ask arguments for deleting an existing targetgroup"""
    targetgroupname = pyt_compat.input_compat("Targetgroupname: ")
    print("")

    return req.requests_targetgroup_del(targetgroupname)

def prompt_targetgroup_addtarget(targetname, targetgroupname):
    """Add a target to a targetgroup"""
    return req.requests_targetgroup_addtarget(targetname, targetgroupname)

def prompt_targetgroup_rmtarget(targetname, targetgroupname):
    """Remove a target from a targetgroup"""
    return req.requests_targetgroup_rmtarget(targetname, targetgroupname)
