#!/bin/bash

# WARNING: this script is made for the default automated installation.

# Launch the passhportd in the virtualenv
nohup /home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/passhportd >> /var/log/passhport/passhportd 2>&1 &

