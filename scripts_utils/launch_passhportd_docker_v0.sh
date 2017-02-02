#!/bin/bash -e
VIRTUAL_ENV_PYTHON="$1"

# Change ownership and rights because it's an external volume mounted by docker
chown -R passhport:passhport /home/passhport/.ssh/
chmod 700 /home/passhport/.ssh/

# Generate keys if they don't exist
if [ ! -r "/home/passhport/.ssh/id_rsa" ]
then
	su - passhport -c "/usr/bin/ssh-keygen -t rsa -b 4096 -N \"\" -f \"/home/passhport/.ssh/id_rsa\""
fi

if [ ! -r "/home/passhport/.ssh/id_ecdsa" ]
then
	su - passhport -c "/usr/bin/ssh-keygen -t ecdsa -b 521 -N \"\" -f \"/home/passhport/.ssh/id_ecdsa\""
fi

if [ ! -e "/home/passhport/certs" ]
then
	su - passhport -c "mkdir /home/passhport/certs"
	su - passhport -c "chmod 700 /home/passhport/certs"
fi

if [ ! -r "/home/passhport/certs/key.pem" ]
then
	su - passhport -c "openssl genrsa -out \"/home/passhport/certs/key.pem\" 4096"
fi

if [ ! -r "/home/passhport/certs/cert.pem" ]
then
	su - passhport -c "openssl req -new -key \"/home/passhport/certs/key.pem\" \
				-config \"/home/passhport/passhport/scripts_utils/openssl-for-passhportd.cnf\" \
				-out \"/home/passhport/certs/cert.pem\" \
				-subj '/C=FR/ST=Ile De France/L=Ivry sur Seine/O=LibrIT/OU=DSI/CN=127.0.0.1' \
				-x509 -days 365 \
				-extensions v3_req"
fi


# Launch the passhportd in the virtualenv
su - passhport -c "\"${VIRTUAL_ENV_PYTHON}\" /home/passhport/passhport/passhportd/passhportd"

