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
    # scp [option] /path/to/my/file user@bastion:targetname//path/on/destination
    # or
    # scp [option] user@bastion:targetname//path/on/destination/file /local/path
    # and we should obtain the target name a line like
    # scp -t /path/on/destination/file 
    # scp -f /path/on/destination/file /local/path
    target = re.findall("([^\s]*)//", originalcmd)
    if target:
        target = target[0]

    cmd = re.sub("\[^\s]*//", "/", originalcmd)

    return [target, cmd]
    
    

def connect(target, filelog, login, sshoptions, originalcmd):
    """ Simply launch the scp connection """

    # The final command should be like
    # ssh -q -t login@target scp -t /path/to/target
    # or to receive
    # ssh -q -t login@target scp -f /path/to/target /local/path/
    # and ssh/scp do magic after that
    cmd = re.sub("scp -(.) ", "ssh -q -t " + login + "@" + target + 
                 " scp -\\1 ", originalcmd )  
    os.system(cmd)
    
    # Print the command on a logfile
    filelog = open(filelog + "-scp.log", "a")
    filelog.write("Original command: " + originalcmd + " - " + "cmd: " + cmd)
    filelog.close()

