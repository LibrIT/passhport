#!/usr/bin/env python
# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals
from builtins import input


def is_int(port):
    """Check if port is an integer"""
    try:
        port = int(port)
    except ValueError:
        return False

    return True


def ask_port(prompt_text):
    """Same as input() but check if user enter an integer"""
    port = input(prompt_text)

    while port and not is_int(port): # Loop until user enter a real number
        print("You didn't enter a number, please try again.")
        port = input(prompt_text)

    return port


def checkaccess(param):
    """Pattern to search targets and check access"""
    pattern = ""

    return{"<pattern>": param}


def prompt_checkaccess():
    """Prompt a pattern to search targets and check access"""
    pattern = input("Pattern used to search the targets to test:")

    return{"<pattern>": pattern}


def prompt_create():
    """Prompt user to obtain data to create a target"""
    port       = ""
    sshoptions = ""
    changepwd  = ""
    sessiondur = ""

    name = input("Name: ")
    hostname = input("Hostname: ")
    targettype = input("Type (default is ssh): ")
    if targettype == "":
        targettype = "ssh"
    login = input("Login (default is root): ")
    if targettype == "ssh":
        port = ask_port("Port (default is 22):")
        sshoptions = input("SSH Options: ")
        changepwd = input("Change the password after each connection (type 'yes' if you really want it): ")
    elif targettype in ["mysql", "postgresql", "oracle", "kubernetes"]:
        port = ask_port("Port:")
        sessiondur = input("Session duration in minutes (default is 12hours):")
    comment = input("Comment: ")


    return {"<name>": name,
        "<hostname>": hostname,
        "--type": targettype,
        "--login": login,
        "--sshoptions": sshoptions,
        "--port": port,
        "--sessiondur": sessiondur,
        "--changepwd": changepwd,
        "--comment": comment}


def create(param):
    """Format param for target creation"""
    targettype = ""
    login = ""
    port = ""
    sshoptions = ""
    changepwd = ""
    comment = ""
    sessiondur = ""

    if "--type" in param:
        targettype = param["--type"]
        if targettype not in ["ssh", "mysql", "oracle", "postgresql"]:
            if len(targettype):
                print ("This type is not supported, ssh will be used. " + \
                       "Please use a type in ssh, mysql, oracle or postgresql")
            targettype = "ssh"

    if "--port" in param:
        if is_int(param["--port"]):
            port = param["--port"]
        else:
            port = 22
            print("Port is unknown, therefore port 22 will be used.")

    if "--sshoptions" in param:
        sshoptions = param["--sshoptions"]

    if "--comment" in param:
        comment = param["--comment"]

    if "--login" in param:
        login = param["--login"]

    if "--changepwd" in param:
        if param["--changepwd"].casefold() == "yes":
            changepwd = "True"
        else:
            changepwd = "False"

    if "--sessiondur" in param:
        sessiondur = param["--sessiondur"]

    print(sessiondur)

    return {"name": param["<name>"],
            "hostname": param["<hostname>"],
            "targettype": targettype,
            "login": login,
            "port": port,
            "sshoptions": sshoptions,
            "changepwd": changepwd,
            "comment": comment,
            "sessiondur": sessiondur}


def prompt_edit(req):
    """Prompt user to obtain data to edit a target"""
    name = input("Name of the target you want to modify: ")
    if not name:
        return False
    
    new_port       = ""
    new_sshoptions = ""
    new_changepwd  = ""
    new_sessiondur = ""

    if req.show("target", {"<name>": name}) == 0:
        new_name = input("New name: ")
        new_hostname = input("New hostname: ")
        new_targettype = input("New type (ssh, mysql, oracle, postgresql): ")
        new_port = ask_port("New port: ")
        if new_targettype == "ssh":
            new_login = input("New Login: ")
            new_changepwd = input("Change the password after each connection (type 'yes' if you really want it): ")
            new_sshoptions = input("New SSH options: ")
        elif new_targettype in ["mysql", "oracle", "postgresql"]:
            new_sessiondur = input("New session duration in minutes:")
        else: # we can't determine which kind of type is, we ask for all
            new_login = input("New Login: ")
            new_changepwd = input("Change the password after each connection (type 'yes' if you really want it, ssh root access only): ")
            new_sshoptions = input("New SSH options: ")
            new_sessiondur = input("New session duration in minutes (mysql, oracle and postgresql only):")
        new_comment = input("New comment: ")
        if len(new_comment.strip()) == 0:
            answer = input("Remove original comment? [y/N]")
            if answer == "y":
                new_comment = "PASSHPORTREMOVECOMMENT"

    return {"<name>": name,
            "--newname": new_name,
            "--newhostname": new_hostname,
            "--newtype": new_targettype,
            "--newlogin": new_login,
            "--newport": new_port,
            "--newsshoptions": new_sshoptions,
            "--newchangepwd": new_changepwd,
            "--newcomment": new_comment,
            "--newsessiondur": new_sessiondur}


def edit(param):
    """Format param for target edition"""
    new_name = ""
    new_hostname = ""
    new_targettype = ""
    new_login = ""
    new_port = ""
    new_sshoptions = ""
    new_changepwd = ""
    new_comment = ""

    if "--newname" in param:
        new_name = param["--newname"]

    if "--newhostname" in param:
        new_hostname = param["--newhostname"]

    if "--newtype" in param:
        new_targettype = param["--newtype"]

    if "--newlogin" in param:
        new_login = param["--newlogin"]

    if "--newport" in param:
        new_port = param["--newport"]

    if "--newsshoptions" in param:
        new_sshoptions = param["--newsshoptions"]

    if "--newchangepwd" in param:
        if param["--newchangepwd"].casefold() == "yes":
            new_changepwd = "True"
        else:
            new_changepwd = "False"

    if "--newcomment" in param:
        new_comment = param["--newcomment"]

    return {"name": param["<name>"],
            "new_name": new_name,
            "new_hostname": new_hostname,
            "new_targettype": new_targettype,
            "new_login": new_login,
            "new_port": new_port,
            "new_sshoptions": new_sshoptions,
            "new_changepwd": new_changepwd,
            "new_comment": new_comment}


def prompt_adduser():
    """Prompt user to obtain data to add a user"""
    username = input("Username: ")
    targetname = input("Targetname: ")

    return {"<username>": username,
            "<targetname>": targetname}


def adduser(param):
    """Format param to add a user"""
    return {"username": param["<username>"],
            "targetname": param["<targetname>"]}


def prompt_rmuser():
    """Prompt user to obtain data to remove a user"""
    username = input("Username: ")
    targetname = input("Targetname: ")

    return {"<username>": username,
            "<targetname>": targetname}


def rmuser(param):
    """Format param to remove a user"""
    return {"username": param["<username>"],
            "targetname": param["<targetname>"]}


def prompt_addusergroup():
    """Prompt user to obtain data to add a usergroup"""
    usergroupname = input("Usergroupname: ")
    targetname = input("Targetname: ")

    return {"<usergroupname>": usergroupname,
            "<targetname>": targetname}


def addusergroup(param):
    """Format param to add a usergroup"""
    return {"usergroupname": param["<usergroupname>"],
            "targetname": param["<targetname>"]}


def prompt_rmusergroup():
    """Prompt user to obtain data to remove a usergroup"""
    usergroupname = input("Usergroupname: ")
    targetname = input("Targetname: ")

    return {"<usergroupname>": usergroupname,
            "<targetname>": targetname}


def rmusergroup(param):
    """Format param to remove a usergroup"""
    return {"usergroupname": param["<usergroupname>"],
            "targetname": param["<targetname>"]}
