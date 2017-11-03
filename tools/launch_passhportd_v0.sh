#!/bin/bash

# WARNING: this script is made for a specific installation

# 1 launch the passhportd in the virtualenv
nohup /home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/passhportd >> /var/log/passhport/passhportd &

