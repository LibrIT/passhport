#!/bin/bash -e
VIRTUAL_ENV_PYTHON="$1"

# Change ownership and rights because it's an external volume mounted by docker
chown -R passhport:passhport /home/passhport/.ssh/
chmod 700 /home/passhport/.ssh/

# Generate keys if they don't exist
if [ ! -r "/home/passhport/.ssh/id_rsa" ]
then
	/usr/bin/ssh-keygen -t rsa -b 4096 -N "" -f "/home/passhport/.ssh/id_rsa"
fi

if [ ! -r "/home/passhport/.ssh/id_ecdsa" ]
then
	/usr/bin/ssh-keygen -t ecdsa -b 521 -N "" -f "/home/passhport/.ssh/id_ecdsa"
fi


# Launch the passhportd in the virtualenv
"${VIRTUAL_ENV_PYTHON}" /home/passhport/passhport/passhportd/passhportd
