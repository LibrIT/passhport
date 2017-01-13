# -*-coding:Utf-8 -*-

"""Contains functions to establish ssh connections"""

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import os

def connect(target, filelog, login, sshoptions):
    """ Simply launch the ssh connection """
    os.system("script -q --timing=" + filelog + ".timing " + filelog + \
              ' -c "ssh ' + login + '@' + target + ' ' + sshoptions +'"')

