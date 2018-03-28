# -*-coding:Utf-8 -*-

"""Contains functions to establish scp connections"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import os, re

def parse(originalcmd):
    """Parse the original scp command written by the user.
       Obtain the target, create the command to pass"""
    # We wait a command like :
    #scp file user@bastion:player//~
    #ssh user@bastion player scp file user@ip:/path/to/file
    #ssh user@bastion player rm file
    #scp [option] /path/to/my/file user@bastion:targetname[//user//ip]//path/on/destination
    # Specific players : 1. If targetname//user//ip//path then it's a scp on a server behind a target
    #                    2. We retrive the file on the target (targetname)
    #                    3. We execute a scp on the target (ssh passhport@target scp file user@ip
    #                    4. We execure a rm on the target (ssh passhport@target rm file
    # or
    #scp [option] user@bastion:targetname//path/on/destination/file /local/path

    # and we should obtain the target name a line like
    # scp -t /path/on/destination/file 
    # scp -f /path/on/destination/file /local/path
    nextuser = ""
    nexttarget = ""
    commandelts = re.split("//", originalcmd)
    target      = re.split(" ", commandelts[0])[-1]
    path        = "/" + commandelts[-1]
    # currently the command is "ssh -t targetname". We want "ssh -t path"
    cmd         = " ".join(re.split(" ", commandelts[0])[:-1]) + " " + path
    if len(commandelts) == 4:
        # Command was like :
        # "scp mygreatfile bastion:target//user//nextserver//path"
        nextuser   = commandelts[1]
        nexttarget = commandelts[2]
    elif len(commandelts) != 2:
        print("Syntax error: there is too many or too few \"//\"." + \
              "It should be like: scp passhport@target//path/to/copy...")
        return False

    return [target, cmd, path, nextuser, nexttarget]
    

def connect(target, filelog, login, sshoptions, originalcmd):
    """ Simply launch the scp connection """
    # The final command should be like
    # ssh -q -t login@target scp -t /path/to/target
    # or to receive
    # ssh -q -t login@target scp -f /path/to/target /local/path/
    # and ssh/scp do magic after that
    cmd = re.sub("scp -(.) ", "ssh -q -t " + login + "@" + target + 
            "scp -\\1 ", originalcmd)  

    # Print the command on a logfile
    filelog = open(filelog + "-scp.log", "a")
    filelog.write("Original command: " + originalcmd + " - " + "cmd: " + cmd)
    filelog.close()
    # Actually execute the command
    os.system(cmd)


def specialconnect(target, filelog, login, sshoptions, originalcmd):
    """Special in the case we need to retrieve a file from a server 
       behind a target: we need to do everything in one pass"""
    
    # We need to put the first scp in a job (with &) because if we don't, 
    # the next scp hangs out and the command never finish.
    # So we wait $! to finish before launching the last scp
    cmd = "ssh -q -t " + sshoptions + " " + login + "@" + target + " " + \
          originalcmd[0] + " && " + \
          "ssh -q -t " + sshoptions + " " + login + "@" + target + " " + \
          originalcmd[1] + " & " + \
          "wait $! && " + \
          "ssh -q -t " + sshoptions + " " + login + "@" + target + " " + \
          originalcmd[2] 

    # Print the command on a logfile
    filelog = open(filelog + "-scp.log", "a")
    filelog.write("Retrive a file - " + "cmd: " + cmd)
    filelog.close()
    # Actually execute the command
    os.system(cmd)

