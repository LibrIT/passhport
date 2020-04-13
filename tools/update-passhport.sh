#!/bin/bash

DEFAULT_PASSHPORT_DIR="/home/passhport/passhport"
DEFAULT_PASSHPORT_RUN_ENV="/home/passhport/passhport-run-env"

PASSHPORT_DIR=$1
PASSHPORT_RUN_ENV=$2

# If no PaSSHport directory has been defined (as first arg), then check the defaults
if [ -z "${PASSHPORT_DIR}" ]
then
	# We should check that the default PaSSHport directory exists and is writeable
	# if not we should exit.
	if [ -w "${DEFAULT_PASSHPORT_DIR}" ]
	then
		PASSHPORT_DIR="${DEFAULT_PASSHPORT_DIR}"
	else
		echo "Error : couldn't find default passhport directory. Please pass passhport"
		echo "directory as first argument to this script."
		exit 1
	fi
# If the defined PaSSHport dir is not writeable, I guess there is a problem
# with the defined 
elif [ ! -w "${PASSHPORT_DIR}" ]
then
	echo "Error : couldn't find the specified passhport directory."
	echo "Please check the passhport path (first arg)."
	exit 1
fi

# If no PaSSHport run-env has been defined (as second arg), the we check the defaults
if [ -z "${PASSHPORT_RUN_ENV}" ]
then
	# We should check that the default PaSSHport run-env (/home/passhport/passhport-run-env)
	# exists and is writeable.
	if [ -w "${DEFAULT_PASSHPORT_RUN_ENV}" ]
	then
		PASSHPORT_RUN_ENV="${DEFAULT_PASSHPORT_RUN_ENV}"
	else
		echo "Error : couldn't find default password. Please pass passhport-run-env directory as second"
		echo "argument to this script."
		exit 1
	fi
# if the defined PaSSHport dir is not writeable, I guess there is a problem w
elif [ ! -d "${PASSHPORT_RUN_ENV}" ]
then
	echo "Error : couldn't find the specified passhport run-env directory."
	echo "Please check the passhport run-env path (second arg)."
	exit 1
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

"${PASSHPORT_RUN_ENV_PIP_BIN}" install sqlalchemy-migrate flask-migrate requests docopt configparser tabulate flask-login ldap3 psutil

cd "${PASSHPORT_DIR}"
git pull origin master || exit 1
cd passhportd
export FLASK_APP=/home/passhport/passhport/passhportd/upgrade-db.py
"${PASSHPORT_RUN_ENV_FLASK_BIN}" db upgrade
if [ $? -ne 0 ]
then
	echo "Upgrade failed."
	exit 1
fi
echo "Upgrade finished."
