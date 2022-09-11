import sys
sys.path.insert(0, '/home/passhport/passhport/passhweb')

import config
from app import app as application

application.config['SECRET_KEY'] = "bsqdttyqiuceccmcmpgg"
