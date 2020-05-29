#!/bin/bash
###############################################################################
#                                                                             #
# Licensed under GPLv3.                                                       #
#                                                                             #
# Used to deploy configuration made on webui.                                 #
#                                                                             #
###############################################################################

BASEDIR="/home/passhport/passhweb/passhconfig"
SPUBSSH="${BASEDIR}/sshkey.pub"
SPRVISSH="${BASEDIR}/sshkey"
SSLCERT="${BASEDIR}/ssl.cert"
SSLKEY="${BASEDIR}/sslkey"
DPUBSSH="/home/passhport/.ssh/sshkey.pub"
DPRIVSSH="/home/passhport/.ssh/sshkey"
SHCONF="/home/passhport/.ssh/config"

# 1. save the configuration
${BASEDIR}/savepassh.sh

# 2. put new ssh key in ssh directory
mv ${SPUBSSH} ${DPUBSSH}
mv ${SPRVISSH} ${DPRIVSSH}
chmod 644 ${DPUBSSH}
chmod 600 ${DPRIVSSH}
# declare this key as primary
grep "^IdentityFile" ${SSHCONF} 
if [ $? -eq 0 ]
    sed -i "s/^IdentityFile/#IdentityFile/" ${SSHCONF}
fi
echo "IdentityFile ${DPUBSSH}" >> ${SSHCONF} 
mv ${SSHCONF} ${SSHCONF}_old
grep -v "#IdentityFile ${SSHCONF}" ${SSHCONF}_old > ${SSHCONF}

# 3. Change apache configuration to add the certificates

# 4. Indicate configuration has been made
touch /home/passhport/passhweb/.neverlaunched

# 5. restart apache

