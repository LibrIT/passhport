# -*-coding:Utf-8 -*-

"""Contains functions to establish ssh connections"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import os, requests, shlex, sys

def connect(target, filelog, login, port, sshoptions, pid, url_passhport, 
            cert, ssh_script, username, originalcmd):
    """ Simply launch the ssh connection or execute the ssh command"""
    if not originalcmd:
        # We replace this process by the connexion to free some memory
        os.execl("/bin/bash", " ",
                 ssh_script,
                 filelog, str(port), login, target, str(pid),
                 url_passhport, cert, username, sshoptions)

    else:
        ssh_args = [
                '/usr/bin/ssh', # argv[0] in C, ignored in execv
                '-p' + str(port),
                login + '@' + target,
            ]
        ssh_args += shlex.split(sshoptions)
        ssh_args += [ originalcmd ]

        newpid = os.fork()
        if newpid == 0:
            os.execv('/usr/bin/ssh', ssh_args)
        else:
            # Close stdin & stdout to not interfere with the ssh command
            sys.stdin.close()
            sys.stdout.close()

            # Log stuff
            f = open(filelog, "w")
            f.write("DIRECT COMMAND --- " + originalcmd + "\n")
            f.close()

            # Wait the end of the child process execution
            os.waitpid(newpid, 0)

            # Log stuff
            url = url_passhport + "connection/ssh/endsession/" + str(pid)
            try:
                if cert != "/dev/null": 
                    r = requests.get(url, verify=cert)
                else:
                    r = requests.get(url)

            except requests.RequestException as e:
                print("ERROR: " + str(e.message), file=sys.stderr)
