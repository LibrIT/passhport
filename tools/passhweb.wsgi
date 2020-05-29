activate_this = '/home/passhport/passhport-run-env/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, '/home/passhport/passhport/passhweb')

import config
from app import app as application

application.config['SECRET_KEY'] = "bsqdttyqiuceccmcmpgg"
