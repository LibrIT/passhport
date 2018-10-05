#!/bin/bash

if [ ! -z "$1" ]
then
	PASSHPORT_DIR=$1
else
	PASSHPORT_DIR="/home/passhport/passhport"
fi

if [ ! -z $2 ]
then
	PASSHPORT_RUN_ENV=$2
else
	PASSHPORT_RUN_ENV="/home/passhport/passhport-run-env"
fi

PASSHPORT_RUN_ENV_PYTHON_BIN="${PASSHPORT_RUN_ENV}/bin/python3"
PASSHPORT_RUN_ENV_FLASK_BIN="${PASSHPORT_RUN_ENV}/bin/flask"
PASSHPORT_RUN_ENV_PIP_BIN="${PASSHPORT_RUN_ENV}/bin/pip"

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
if [ ! -x "${PASSHPORT_RUN_ENV_PIP_BIN}" ]
then
       echo "\"${PASSHPORT_RUN_ENV_PIP_BIN}\" does not exist, or is not executable."
       exit 1
fi

cd "${PASSHPORT_DIR}"
echo -n "Do you want to \"git pull\" from github ? Y/n"
read ANSWER
ANSWER=`echo "${ANSWER}" | tr '[:upper:]' '[:lower:]'`

if [ "${ANSWER}" == y ] || [ -z "${ANSWER}" ]
then
	git pull origin master || exit 1
fi

cd "${PASSHPORT_DIR}/passhportd"

export FLASK_APP=/home/passhport/passhport/passhportd/upgrade-db.py
"${PASSHPORT_RUN_ENV_FLASK_BIN}" db migrate
if [ $? -ne 0 ]
then
	echo "Database migration file creation failed."
	exit 1
fi
echo "Database migration file successfully created."
