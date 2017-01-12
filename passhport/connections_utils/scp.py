# -*-coding:Utf-8 -*-

"""Contains functions to establish scp connections"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import os, random, crypt, re

def parse(originalcmd):
    """Parse the original scp command written by the user.
       Obtain the target, create the command to pass"""
    # We wait a command like :
    # scp [option] /path/to/my/file user@bastion:targetname//path/on/destination
    # or
    # scp [option] user@bastion:targetname//path/on/destination/file /local/path
    # and we should obtain the target name a line like
    # scp -t @targetname:path/on/destination/file /local/path
    target = re.findall("(\w*)//", originalcmd)
    if target:
        target = target[0]

    cmd = re.sub("\w*//", "@" + target + ":/", originalcmd)

    return [target, cmd]
    
    

def connect(filelog, login, sshoptions, originalcmd):
    """ Simply launch the scp connection """

    cmd = re.sub("scp -t ", "scp -q -t " + sshoptions + " " + login, 
                 originalcmd)
    print(cmd)
    os.system(cmd)
    
    # Print the command on a logfile
    filelog = open(filelog + "-scp.log", "a")
    filelog.write(originalcmd)
    filelog.close()

