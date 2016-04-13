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
function test_basic_dependencies {
   # Passhport is a python software
   which python &> /dev/null
   if [ $? = 1 ]
   then
      echo "Error: you need python compiler on your PATH."
      exit 126
   fi 
   
   echo -n "Currently using "
   python --version
}


###########################
# Check Python dependencies
###########################
function test_python_dependencies {
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
      return 1
   else
      return 0
   fi
}

function check_if_passhport_system_user_exists {
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
      return 0
   fi
}

function check_if_passhport_system_group_exists {
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
      return 0
   fi
}

function check_if_authorized_keys_exists {
   echo -n "Checking if \"${HOMEDIR}/.ssh/authorized_keys2\" already exists... "
   if [ -f "${HOMEDIR}/.ssh/authorized_keys2" ]
   then
      echo "Error !"
      echo "The file \"${HOMEDIR}/.ssh/authorized_keys2\" already exist. Please create another user or delete/move the file away."
      exit 126
   else
      echo "doesn't exist ! (good)"
      return 0
   fi
}

function check_if_passhport_database_already_exists {
   echo -n "Checking if passhport database (${DATADIR}/app.db) already exist... "
   if [ -f "${DATADIR}/app.db" ]
   then
      echo "Error : the database \"${DATADIR}/app.db\" already exist. Please delete the file."
      exit 126
   else
      echo "doesn't exist ! (good)"
      return 0
   fi
}
   

#################
# Create the user
#################
function add_passhport_system_user_and_group {
   echo -n "Creating the ${USERNAME} user on the system... "
   useradd --create-home --base-dir "${HOMEDIR}" --home-dir "${HOMEDIR}" --user-group --password ${PASSWORD} ${USERNAME} > /dev/null 2>&1
   if [ $? -eq 0 ]
   then
      echo "done."
      return 0
   else
      echo "Error while creating system user \"${USERNAME}\"."
      exit 126   
   fi
}
   
##################
# Install binaries
##################
function install_binaries {
   echo -n "Installing server-side binaries... "
   mkdir -p "${SERVERBINDIR}"
   cp -r passhportd/* "${SERVERBINDIR}/."
   if [ $? -eq 0 ]
   then
      echo "done."
      return 0
   else
      echo "Error while copying server-side binaries."
      exit 126   
   fi
   chown -R ${USERNAME}:${GROUPNAME} "${SERVERBINDIR}"
   
   echo -n "Installing admin binaries... "
   mkdir -p "${ADMINBINDIR}"
   cp -r passhport_admin/* "${ADMINBINDIR}/."
   if [ $? -eq 0 ]
   then
      echo "done."
      return 0
   else
      echo "Error while copying admin binaries."
      exit 126   
   fi
   chown -R ${USERNAME}:${GROUPNAME} "${ADMINBINDIR}"
}   
 

#####################
# Initialize database
#####################
function database_initialization {
   echo -n "Initialize database... "
   su ${USERNAME} -c "${SERVERBINDIR}/db_create.py"
   if [ $? -eq 0 ]
   then
      echo "done."
      return 0
   else
      echo "Error while creating database."
      exit 126   
   fi
}


#####################
# Initialize passhport ssh-keys
#####################
function passhport_ssh_keys_initialization {
   echo -n "Initialize passhport ecdsa ssh-key..."
   su - ${USERNAME} -c "mkdir ${HOMEDIR}/.ssh/"
   su - ${USERNAME} -c "chmod 700 ${HOMEDIR}/.ssh/"
   su - ${USERNAME} -c "ssh-keygen -f ${HOMEDIR}/.ssh/id_ecdsa -t ecdsa -b 521 -q -N \"\""
   if [ $? -eq 0 ]
   then
      echo "done."
      echo "Your passhport ECDSA key is 521 bits long (very strong, will not work on very old servers), stored in \"${HOMEDIR}/.ssh/id_ecdsa\""
      echo "Your passhport ecdsa public key is :"
      echo "============================"
      cat "${HOMEDIR}/.ssh/id_ecdsa.pub"
      echo "============================"
   else
      echo "Error while creating database."
      exit 126   
   fi
   echo -n "Initialize passhport rsa ssh-key..."
   su - ${USERNAME} -c "ssh-keygen -f ${HOMEDIR}/.ssh/id_rsa -t rsa -b 4096 -q -N \"\""
   if [ $? -eq 0 ]
   then
      echo "done."
      echo "Your passhport RSA key is 4096 bits long, stored in \"${HOMEDIR}/.ssh/id_rsa\""
      echo "Your passhport RSA public key is :"
      echo "============================"
      cat "${HOMEDIR}/.ssh/id_rsa.pub"
      echo "============================"
   else
      echo "Error while creating rsa ssh-key..."
      exit 126   
   fi
}

function display_finish_info {
   echo ""
   echo "==> Great ! All actions finished successfully !"
   echo "INFO : Server scripts directory is \"${SERVERBINDIR}\""
   echo "INFO : Administration scripts directory is \"${ADMINBINDIR}\""
   echo "INFO : Database directory is : \"${DATADIR}\""
   echo ""
   echo "Next thing you should do : "
   echo " - launch passhportd daemon \"su - ${USERNAME} -c '${SERVERBINDIR}/passhportd &'\""
   echo " - create your first user \"su - ${USERNAME} -c '${ADMINBINDIR}/passhport-admin user create'\""
}

#######
# MAIN
#######
test_basic_dependencies
DIST_PACKAGE_LIST=""
MISSED_DEPENDENCIE_COUNT=0
MISSED_DEPENDENCIE_LIST=""
DIST_PACKAGE_LIST=""
ALLREADY_TRIED_TO_INSTALL=0
test_python_dependencies
if [ $? -ne 0 ]
then
	echo -n "Do you want this script install all the missing dependencies ? [Y/n]"
	read USER_RESPONSE
	if [ "${USER_RESPONSE}" == 'Y' ]
	then
		if $(which yum > /dev/null 2>&1) 
		then
			yum install ${DIST_PACKAGE_LIST}
		else
			apt-get install ${DIST_PACKAGE_LIST}
		fi
	else
		echo 'No problem ! Try to install those dependencies manually, then try to run this installer script again.'
		echo 'Bye ! :)'
	fi
	test_python_dependencies
	if [ $? -ne 0 ]
	then
		echo "Couldn't install the dependency… To bad. Try to install those dependencies manually."
		echo "Python dependency : ${MISSED_DEPENDENCIE_LIST}"
		return 1
	fi
fi

check_if_passhport_system_user_exists
check_if_passhport_system_group_exists
check_if_authorized_keys_exists
check_if_passhport_database_already_exists
add_passhport_system_user_and_group
install_binaries
database_initialization
passhport_ssh_keys_initialization
display_finish_info
