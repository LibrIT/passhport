# -*-coding:Utf-8 -*-

"""Contains functions that interpret commmands from the CLI and call request functions for user's management"""

import python_compat as pyt_compat
import requests_functions as req

def list():
    """List all users in the database"""
    return req.list()

def search(pattern):
    """Search a user according to the pattern"""
    return req.search(pattern)

def create():
    """Ask arguments for user creation"""
    email   = pyt_compat.input_compat("Email: ")
    comment = pyt_compat.input_compat("Comment: ")
    sshkey  = pyt_compat.input_compat("SSHKey: ")

    return req.create(email, comment, sshkey)

def show():
    """Ask arguments for showing user"""
    email = pyt_compat.input_compat("Email: ")

    return req.show(email)

def edit():
    """Ask arguments for editing an existing user"""
    email = pyt_compat.input_compat("Email of the user you want to modify: ")

    if req.show(email) == 0:
        new_email   = pyt_compat.input_compat("New email: ")
        new_comment = pyt_compat.input_compat("New comment: ")
        new_sshkey  = pyt_compat.input_compat("New SSH key: ")

        return req.edit(email, new_email, new_comment, new_sshkey)

def delete():
    """Ask arguments for deleting an existing user"""
    email = pyt_compat.input_compat("Email: ")

    return req.delete(email)
