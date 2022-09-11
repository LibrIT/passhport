#!/bin/bash

# WARNING: this script is made for dev purposes.

# Launch the passhportd in the virtualenv
nohup /home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/passhportd >> /var/log/passhport/passhportd 2>&1 &

