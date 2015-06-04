#!/usr/bin/env bash
# Installation script for Debian
# The script:
# Check distribution type
# Check if dependencies are met
# Check if the application has already been installed
# Initialize the database
# Create the first admin


############
# Variables
############ 
#Supported distributions.
DISTRIBUTIONS="Debian GNU/Linux 7 Debian GNU/Linux 8"
#Python includes needed for the work
DEPENDENCIES=( 'from docopt import docopt' 'from flask import Flask' 'from flask.ext.sqlalchemy import SQLAlchemy' 'from migrate.versioning import api' )

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
# Testing Authorized keys file
# Testing database (standard one...)

#####################
# Initialize database
#####################
