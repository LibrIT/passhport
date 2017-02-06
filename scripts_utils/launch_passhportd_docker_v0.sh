#!/bin/bash -e
VIRTUAL_ENV_PYTHON="$1"

# Change ownership and rights because it's an external volume mounted by docker
chown -R passhport:passhport /home/passhport/.ssh/
chmod 700 /home/passhport/.ssh/

# Generate keys if they don't exist
if [ ! -r "/home/passhport/.ssh/id_rsa" ]
then
	echo "Generating id_rsa key pair…"
	su - passhport -c "/usr/bin/ssh-keygen -t rsa -b 4096 -N \"\" -f \"/home/passhport/.ssh/id_rsa\""
fi

if [ ! -r "/home/passhport/.ssh/id_ecdsa" ]
then
	echo "Generating id_ecdsa key pair…"
	su - passhport -c "/usr/bin/ssh-keygen -t ecdsa -b 521 -N \"\" -f \"/home/passhport/.ssh/id_ecdsa\""
fi

if [ ! -e "/home/passhport/var/app.db" ]
then
	echo "Passhportd database does not exist. Creating database…"
	if [ ! -e "/home/passhport/var" ]
	then
		su - passhport -c "mkdir \"/home/passhport/var\""
	fi
	chown -R passhport:passhport "/home/passhport/var"
	su - passhport -c "\"${VIRTUAL_ENV_PYTHON}\" /home/passhport/passhport/passhportd/db_create.py"
fi

if [ ! -e "/home/passhport/certs" ]
then
	echo "Certification directory does not exist. Creating them…"
	su - passhport -c "mkdir /home/passhport/certs"
	su - passhport -c "chmod 700 /home/passhport/certs"
fi

if [ ! -r "/home/passhport/certs/key.pem" ]
then
	echo "Generating passhportd web API key…"
	su - passhport -c "openssl genrsa -out \"/home/passhport/certs/key.pem\" 4096"
fi

if [ ! -r "/home/passhport/certs/cert.pem" ]
then
	echo "Creating passhportd web API certificate…"
	# Certificat generation assistant
	IS_HOSTNAME_VALID=0
	while [ ${IS_HOSTNAME_VALID} -eq 0 ]
	do
		echo "What will be the hostname of passhportd ? (to generate a pseudo-valid certificat)"
		read PASSHPORTD_HOSTNAME
		echo "${PASSHPORTD_HOSTNAME}" | perl -pe 'exit 0 if /^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$/; exit 1'
		if [ $? -eq 0 ]
		then
			IS_HOSTNAME_VALID=1
		else
			echo "Error : hostname is not valid"
		fi
	done
	IP_GATEWAY=`/sbin/ip route|awk '/default/ { print $3 }'`
	echo "DNS.3 = ${IP_GATEWAY}" >> "/home/passhport/passhport/scripts_utils/openssl-for-passhportd.cnf" 
	echo "DNS.4 = ${PASSHPORTD_HOSTNAME}" >> "/home/passhport/passhport/scripts_utils/openssl-for-passhportd.cnf" 
	su - passhport -c "openssl req -new -key \"/home/passhport/certs/key.pem\" \
				-config \"/home/passhport/passhport/scripts_utils/openssl-for-passhportd.cnf\" \
				-out \"/home/passhport/certs/cert.pem\" \
				-subj '/C=FR/ST=Ile De France/L=Ivry sur Seine/O=LibrIT/OU=DSI/CN=${PASSHPORTD_HOSTNAME}' \
				-x509 -days 365 -sha256\
				-extensions v3_req"
fi


# Launch the passhportd in the virtualenv
su - passhport -c "\"${VIRTUAL_ENV_PYTHON}\" /home/passhport/passhport/passhportd/passhportd"

