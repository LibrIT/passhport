#!/usr/bin/env bash
# Installation script for Debian
# The script:
# Check distribution type
# Check if dependencies are met
# Check if the application has already been installed
# Initialize the database
# Create the first admin


# First of all: must be launched as root
if [ $EUID -ne 0 ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi



############
# Variables
############ 
#Supported distributions.
DISTRIBUTIONS="Debian GNU/Linux 7 Debian GNU/Linux 8"
#Python includes needed for the work
PYTHON_BIN=`which python`
DEPENDENCIES=( 'from docopt import docopt' 'from flask import Flask' 'from flask.ext.sqlalchemy import SQLAlchemy' 'from migrate.versioning import api' 'from builtins import input' 'import requests')
USERNAME="passhport"
GROUPNAME="${USERNAME}"
HOMEDIR="/home/${USERNAME}"
ADMINBINDIR="${HOMEDIR}/adminbin"
SERVERBINDIR="${HOMEDIR}/serverbin"
DATADIR="${HOMEDIR}/var"
PASSWORD="$(openssl passwd -crypt $( < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c8))" #crypted
DIRNAME="$(dirname $0)"

###################
# Distribution type
###################
distrib="$( sed "s/ \\\n \\\l//" /etc/issue )"
echo ${DISTRIBUTIONS} | grep "${distrib}"  &> /dev/null
result=?$
if [ ${result} = 1 ]
then
   echo "Error: Passhport is validated only on this distributions: ${DISTRIBUTION}"
   exit 126
fi

##############
# Dependencies
##############
# Passhport is a python software
which python &> /dev/null
if [ $? = 1 ]
then
   echo "Error: you need python compiler on your PATH."
   exit 126
fi 

echo -n "Currently using "
python --version

# We test to import the different librairies with python
MISSED_DEPENDENCIE_COUNT=0
MISSED_DEPENDENCIE_LIST=""
DIST_PACKAGE_LIST=""
for DEPENDENCIE in "${DEPENDENCIES[@]}"
do
   MISSING_PYTHON_MODULE=`echo ${DEPENDENCIE} | awk '{ print $2 }'`
   ${PYTHON_BIN} -c "${DEPENDENCIE}" &> /dev/null
   EXIT_STATUS=$?
   if [ "${EXIT_STATUS}" == "1" ]
   then
      MISSED_DEPENDENCIE_COUNT=`expr ${MISSED_DEPENDENCIE_COUNT} + 1`
      echo "Error: Passhport missing a dependencie: ${MISSING_PYTHON_MODULE}"
      MISSED_DEPENDENCIE_LIST="${MISSING_PYTHON_MODULE} ${MISSED_DEPENDENCIE_LIST}"
      if [ "${MISSING_PYTHON_MODULE}" == "docopt" ]
      then
         DIST_PACKAGE_LIST="python-docopt ${DIST_PACKAGE_LIST}"
      elif [ "${MISSING_PYTHON_MODULE}" == "flask" ]
      then
         DIST_PACKAGE_LIST="python-flask ${DIST_PACKAGE_LIST}"
      elif [ "${MISSING_PYTHON_MODULE}" == "flask.ext.sqlalchemy" ]
      then
         DIST_PACKAGE_LIST="python-flask-sqlalchemy ${DIST_PACKAGE_LIST}"
      elif [ "${MISSING_PYTHON_MODULE}" == "migrate.versioning" ]
      then
         DIST_PACKAGE_LIST="python-migrate ${DIST_PACKAGE_LIST}"
      elif [ "${MISSING_PYTHON_MODULE}" == "builtins" ]
      then
         DIST_PACKAGE_LIST="python2-future ${DIST_PACKAGE_LIST}"
      elif [ "${MISSING_PYTHON_MODULE}" == "requests" ]
      then
         DIST_PACKAGE_LIST="python-requests ${DIST_PACKAGE_LIST}"
      fi
   fi
done

if [ ${MISSED_DEPENDENCIE_COUNT} -ne 0 ]
then
   echo "You're missing ${MISSED_DEPENDENCIE_COUNT} dependencies."
   echo "Maybe you have librairies for python 3 and you're using python 2.7"
   echo "Check your environnement to knows the default python version on your distribution".
   echo ""
   echo "You may use this commande to install those package (enable EPEL repo on redhat/centos/fedora) :"
   echo "For RPM based distribution : yum install epel-release && yum install ${DIST_PACKAGE_LIST}"
   echo "For DEB based distribution : apt-get install ${DIST_PACKAGE_LIST}"
   echo "Try to install those dependencies and launch this install process again."
   exit 126
fi

#################
# Old application
#################
# Testing the user existence
echo -n "Checking if \"${USERNAME}\" user already exist on the system... "
getent passwd | grep "^${USERNAME}:" > /dev/null 2>&1
if [ $? -eq 0 ]
then
   echo "Error !"
   echo "The user \"${USERNAME}\" already exist..."
   echo "Tip : remove the user \"${USERNAME}\" from /etc/passwd"
   exit 126
else
   echo "done."
fi

# Testing group existence
echo -n "Checking if \"${GROUPNAME}\" group already exist on the system... "
grep "^${GROUPNAME}:" /etc/group > /dev/null 2>&1
if [ $? -eq 0 ]
then
   echo "Error !"
   echo "The group \"${GROUPNAME}\" already exist..."
   echo "Tip : remove the group \"${GROUPNAME}\" from /etc/group"
   exit 126
else
   echo "done."
fi

# Testing Authorized keys file
echo -n "Checking if \"${HOMEDIR}/.ssh/authorized_keys2\" already exists... "
if [ -f "${HOMEDIR}/.ssh/authorized_keys2" ]
then
   echo "Error !"
   echo "The file \"${HOMEDIR}/.ssh/authorized_keys2\" already exist. Please create a new user or delete the file."
   exit 126
else
   echo "doesn't exist ! (good)"
fi

# Testing database (standard one...)
echo -n "Checking if passhport database (${DATADIR}/app.db) already exist... "
if [ -f "${DATADIR}/app.db" ]
then
   echo "Error : the database \"${DATADIR}/app.db\" already exist. Please delete the file."
   exit 126
else
   echo "doesn't exist ! (good)"
fi

#################
# Create the user
#################
echo -n "Creating the ${USERNAME} user on the system... "
useradd --create-home --base-dir "${HOMEDIR}" --home-dir "${HOMEDIR}" --user-group --password ${PASSWORD} ${USERNAME} > /dev/null 2>&1
if [ $? -eq 0 ]
then
   echo "done."
else
   echo "Error while creating system user \"${USERNAME}\"."
   exit 126   
fi
#chown -R ${USERNAME}:${GROUPNAME} ${HOMEDIR}

##################
# Install server binaries
##################
echo -n "Installing server-side binaries... "
mkdir -p "${SERVERBINDIR}"
cp -r passhportd/* "${SERVERBINDIR}/."
if [ $? -eq 0 ]
then
   echo "done."
else
   echo "Error while copying server-side binaries."
   exit 126   
fi
chown -R ${USERNAME}:${GROUPNAME} "${SERVERBINDIR}"

##################
# Install admin binaries
##################
echo -n "Installing admin binaries... "
mkdir -p "${ADMINBINDIR}"
cp -r passhport_admin/* "${ADMINBINDIR}/."
if [ $? -eq 0 ]
then
   echo "done."
else
   echo "Error while copying admin binaries."
   exit 126   
fi
chown -R ${USERNAME}:${GROUPNAME} "${ADMINBINDIR}"


#####################
# Initialize database
#####################
echo -n "Initialize database... "
SOURCE_DIR=`pwd`
su ${USERNAME} -c "${SERVERBINDIR}/db_create.py"
if [ $? -eq 0 ]
then
   echo "done."
else
   echo "Error while creating database."
   exit 126   
fi

#######################
# Create the first user
#######################
#TODO

echo ""
echo "==> Great ! All actions finished successfully !"
echo "INFO : Server scripts directory is \"${SERVERBINDIR}\""
echo "INFO : Administration scripts directory is \"${ADMINBINDIR}\""
echo "INFO : Database directory is : \"${DATADIR}\""
echo ""
echo "Next thing you should do : "
echo " - launch passhportd daemon \"su - ${USERNAME} -c '${SERVERBINDIR}/passhportd &'\""
echo " - create your first user \"su - ${USERNAME} -c '${ADMINBINDIR}/passhport-admin user create'\""
