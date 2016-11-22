#!/bin/bash

# WARNING: this scripts works for a specific installation only

# 0 First install some dependancies
su -c "apt install python3-docopt python3-flask python3-flask-sqlalchemy python3 python-flask-migrate python3-flask python3-flask-sqlalchemy python3-pip python3-virtualenv git"

# 1 Download code localy
git clone https://github.com/elg/passhport.git

# 2 Initialize the virtual environement
python3 -m venv /home/passhport/passhport-run-env
/home/passhport/passhport-run-env/bin/pip install pymysql sqlalchemy-migrate flask-migrate requests docopt

# 3 Initialize the database
/home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/db_create.py

# 4 Create passhport ssh-key to put on different servers
ssh-keygen -t rsa -N ""  -f /home/passhport/.ssh/id_rsa

# 5 Create the log directory on system
su -c "mkdir -p /var/log/passhport/; chown passhport:passhport /var/log/passhport/"
