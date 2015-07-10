#!/usr/bin/env python
# -*-coding:Utf-8 -*-

from . import python_compat as pyt_compat

def is_int(port):
    """Check if port is an integer"""
    try:
        port = int(port)
    except ValueError:
        return False

    return True


def ask_port(prompt_text):
    """Same as input() but check if user enter an integer"""
    port = pyt_compat.input_compat(prompt_text)

    while port and not is_int(port):  # Loop until user enter a real number
        print("You didn't enter a number, please try again.")
        port = pyt_compat.input_compat(prompt_text)

    return port


def prompt_create():
    """Prompt user to obtain data to request"""
    name = pyt_compat.input_compat("Name: ")
    hostname = pyt_compat.input_compat("Hostname: ")
    port = ask_port("Port: ")
    sshoptions = pyt_compat.input_compat("SSH Options: ")
    servertype = pyt_compat.input_compat("Server type: ")
    autocommand = pyt_compat.input_compat("Autocommand: ")
    comment = pyt_compat.input_compat("Comment: ")

    return {"<name>": name,
        "<hostname>": hostname,
        "--sshoptions": sshoptions,
        "--port": port,
        "--servertype": servertype,
        "--autocommand": autocommand,
        "--comment": comment}


def create(param):
    """Format param for target creation"""
    port = ""
    sshoptions = ""
    servertype = ""
    autocommand = ""
    comment = ""

    if "--port" in param:
        if is_int(param["--port"]):
            port = param["--port"]
        else:
            print("Port is unknown, therefore port 22 will be used.")

    if "--sshoptions" in param:
        sshoptions = param["--sshoptions"]
    if "--servertype" in param:
        servertype = param["--servertype"]
    if "--autocommand" in param:
        autocommand = param["--autocommand"]
    if "--comment" in param:
        comment = param["--comment"]

    return {"name": param["<name>"],
            "hostname": param["<hostname>"],
            "port": port,
            "sshoptions": sshoptions,
            "servertype": servertype,
            "autocommand": autocommand,
            "comment": comment}


def prompt_edit():
    """Prompt user to obtain data to request"""
    name = pyt_compat.input_compat("Name of the target you want to modify: ")

    if req.show("target", {"<name>": name}) == 0:
        new_name = pyt_compat.input_compat("New name: ")
        new_hostname = pyt_compat.input_compat("New hostname: ")
        new_port = ask_port("New port: ")
        new_sshoptions = pyt_compat.input_compat("New SSH options: ")
        new_servertype = pyt_compat.input_compat("New server type: ")
        new_autocommand = pyt_compat.input_compat("New autocommand: ")
        new_comment = pyt_compat.input_compat("New comment: ")


    return {"<name>": name,
            "--newname": new_name,
            "--newhostname": new_hostname,
            "--newport": new_port,
            "--newsshoptions": new_sshoptions,
            "--newservertype": new_servertype,
            "--newautocommand": new_autocommand,
            "--newcomment": new_comment}


def edit(param):
    """Format param for target edition"""
    new_name = ""
    new_hostname = ""
    new_port = ""
    new_sshoptions = ""
    new_servertype = ""
    new_autocommand = ""
    new_comment = ""

    if "--newname" in param:
        new_name = param["--newname"]
    if "--newhostname" in param:
        new_hostname = param["--newhostname"]
    if "--newport" in param:
        new_port = param["--newport"]
    if "--newsshoptions" in param:
        new_sshoptions = param["--newsshoptions"]
    if "--newservertype" in param:
        new_servertype = param["--newservertype"]
    if "--newautocommand" in param:
        new_autocommand = param["--newautocommand"]
    if "--newcomment" in param:
        new_comment = param["--newcomment"]


    return {"name": param["<name>"],
            "new_name": new_name,
            "new_hostname": new_hostname,
            "new_port": new_port,
            "new_sshoptions": new_sshoptions,
            "new_servertype": new_servertype,
            "new_autocommand": new_autocommand,
            "new_comment": new_comment}
