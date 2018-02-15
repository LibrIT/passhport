#!/bin/bash

PASSHPORT_DIR=$1
PASSHPORT_RUN_ENV=$2
PASSHPORT_RUN_ENV_PYTHON_BIN="${PASSHPORT_RUN_ENV}/bin/python3"
PASSHPORT_RUN_ENV_FLASK_BIN="${PASSHPORT_RUN_ENV}/bin/flask"

ps auxf | grep -e "passhport[d]$" &>/dev/null
if [ $? -eq 0 ]
then
	echo "passhportd daemon seems to be running. Please stop it and launch this script again."
	exit 1
fi

if [ ! -x "${PASSHPORT_RUN_ENV_PYTHON_BIN}" ]
then
	echo "\"${PASSHPORT_RUN_ENV_PYTHON_BIN}\" does not exist, or is not executable."
	exit 1
fi
if [ ! -x "${PASSHPORT_RUN_ENV_FLASK_BIN}" ]
then
	echo "\"${PASSHPORT_RUN_ENV_FLASK_BIN}\" does not exist, or is not executable."
	exit 1
fi

cd "${PASSHPORT_DIR}"
git pull origin master|| exit 1
cd passhportd
export FLASK_APP=/home/passhport/passhport/passhportd/upgrade-db.py
/home/passhport/passhport-run-env/bin/flask db upgrade
if [ $? -ne 0 ]
then
	echo "Upgrade failed."
	exit 1
fi
echo "Upgrade finished."
