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
DEPENDENCIES=( 'from docopt import docopt' 'from flask import Flask' 'from flask.ext.sqlalchemy import SQLAlchemy' 'from migrate.versioning import api' )
USERNAME="passhport"
HOMEDIR="/home/${USERNAME}"
DATABASE="${HOMEDIR}/app.db"
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
    echo "Error: Passhport is validated only on this distirbutions: ${DISTRIBUTION}"
    exit 126
fi

##############
# Dependencies
##############
# Passhport is a python software
which python &> /dev/null
if [ $? = 1 ]
then
    echo "Error: common, you NEED a python on your PATH."
    exit 126
fi

# We test to import the different librairies with python
for dependence in "${DEPENDENCIES[@]}"
do
    /usr/bin/env python -c "${dependence}" &> /dev/null
    result=$?
    if [ "$result" = "1" ]
    then
        echo "Error: Passhport missing a dependence to do this: ${dependence}"
        exit 126
    fi
done

#################
# Old application
#################
# Testing the user existence
getent passwd | grep "^${USERNAME}:"
if [ $? = 0 ]
then
    echo "Error: The user ${USERNAME} already exist..."
    exit 126
fi
        
# Testing Authorized keys file
if [ -f ${HOMEDIR}/.ssh/authorized_keys2 ]
then
    echo "The file ${HOMEDIR}/.ssh/authorized_keys2 already exist. Please create a new user or delete the file."
    exit 126
fi

# Testing database (standard one...)
if [ -f ${DATABASE} ]
then
    echo "The database ${DATABASE} already exist. Please delete the file."
    exit 126
fi

#################
# Create the user
#################
echo "Creating the ${USERNAME} user on the system"
useradd -U -p ${PASSWORD} ${USERNAME}
chown -R ${USERNAME}: ${BASEDIR}

#####################
# Initialize database
#####################
echo "Initialize database"
curdir=${pwd}
su ${USERNAME}
cd ${curdir}
cd ${DIRNAME}
./db_create.py

#######################
# Create the first user
#######################
#TODO

echo "All actions done."


