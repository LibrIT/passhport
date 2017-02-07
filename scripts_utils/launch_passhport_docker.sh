#!/bin/bash

echo "What is the hostname of your passhportd host ?"
read PASSHPORTD_HOSTNAME

echo "172.17.0.1 ${PASSHPORTD_HOSTNAME}" >> /etc/hosts

sed -ie "s#url_passhport =.*#url_passhport = \"https://${PASSHPORTD_HOSTNAME}:5000/\"#" /home/passhport/passhport/passhport/passhport

echo "Launching sshd daemon…"
/usr/sbin/sshd -D
