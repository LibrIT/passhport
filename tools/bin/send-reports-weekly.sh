#! /bin/bash

PASSHPORT_HOST_WITH_PORT=$1
RECIPIENT=$2

wget --no-check-certificate -qO - https://${PASSHPORT_HOST_WITH_PORT}/reporting/weekly/4 | /usr/bin/mail -s "PaSSHport weekly report" ${RECIPIENT}

