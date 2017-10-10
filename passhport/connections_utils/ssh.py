# -*-coding:Utf-8 -*-

"""Contains functions to establish ssh connections"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import os

def connect(target, filelog, login, port, sshoptions, originalcmd):
    """ Simply launch the ssh connection or execute the ssh command"""
    if not originalcmd:
        os.system("script -q --timing=" + filelog + ".timing " + filelog + \
                ' -c "ssh -t -p ' + str(port) + " " + login + '@' + target + \
                ' ' + sshoptions + '"')
    else:
        os.system("echo \"DIRECT COMMAND --- " + \
                  originalcmd + "\" >" + filelog + \
                  ' && ssh -p ' + str(port) + " " + login + '@' + target + \
                  ' ' + sshoptions + " " + originalcmd )

