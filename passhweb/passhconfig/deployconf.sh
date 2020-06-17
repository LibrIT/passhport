#!/bin/bash
###############################################################################
#                                                                             #
# Licensed under GPLv3.                                                       #
#                                                                             #
# Used to deploy configuration made on webui.                                 #
#                                                                             #
###############################################################################

BASEDIR="/home/passhport/passhport/passhweb/passhconfig"
URL=$1
SPUBSSH="${BASEDIR}/sshkey.pub"
SPRVISSH="${BASEDIR}/sshkey"
SSLCERT="${BASEDIR}/server.cert"
SSLKEY="${BASEDIR}/server.key"
DPUBSSH="/home/passhport/.ssh/sshkey.pub"
DPRIVSSH="/home/passhport/.ssh/sshkey"
SSHCONF="/home/passhport/.ssh/config"
HTTPD_CONF="/etc/apache2/sites-available/passhweb.conf"

# 1. save the configuration
${BASEDIR}/savepassh.sh

# 2. put new ssh key in ssh directory
mv ${SPUBSSH} ${DPUBSSH}
mv ${SPRVISSH} ${DPRIVSSH}
chmod 644 ${DPUBSSH}
chmod 600 ${DPRIVSSH}

# declare this key as primary
mv ${SSHCONF} ${SSHCONF}_old
grep -v "^IdentityFile" ${SSHCONF}_old > ${SSHCONF}
echo -e "\nIdentityFile ${DPUBSSH}" >> ${SSHCONF} 

# 3. Put certificate in ~/certs
mkdir -p ~/certs
mv ${SSLCERT} ~/certs/server.cert
mv ${SSLKEY} ~/certs/server.key
chmod a+r ~/certs/server.cert
chmod a+r ~/certs/server.key

# 4. Change apache configuration
sudo mv ${HTTPD_CONF} ${HTTPD_CONF}_old
sed "s/passhweburl/${URL}/" ${BASEDIR}/passhweb.conf.template > ${BASEDIR}/passhweb.conf
sudo mv ${BASEDIR}/passhweb.conf ${HTTPD_CONF}

# 5. Indicate configuration has been made
touch /home/passhport/passhweb/.neverlaunched

# 6. restart apache (On passhport VM mode it should works, else modify the sudoers)
sudo systemctl restart apache2
