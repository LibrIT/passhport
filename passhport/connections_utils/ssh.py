# -*-coding:Utf-8 -*-

"""Contains functions to establish ssh connections"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import os

def connect(target, filelog, login, port, sshoptions, pid, url_passhport, cert, ssh_script, originalcmd):
    """ Simply launch the ssh connection or execute the ssh command"""
    if not originalcmd:
        # We replace this process by the connexion to free some memory
        os.execl("/bin/bash", " ",
                 ssh_script,
                 filelog, str(port), login, target, str(pid),
                 url_passhport, cert, sshoptions)

    else:
        f = open(filelog, "w")
        f.write("DIRECT COMMAND --- " + originalcmd)
        f.close()
        os.system('ssh -p ' + str(port) + " " + login + '@' + target + \
                  ' ' + sshoptions + " '" + originalcmd + "'" )
        
