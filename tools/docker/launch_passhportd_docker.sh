#!/bin/bash -e
PYTHON_ENV_RUNTIME="$1"

echo "VIRTUAL_ENV_PYTHON=$PYTHON_ENV_RUNTIME"


############
# SSH KEYS #
############
# Change ownership and rights because it's an external volume mounted by docker
chmod 700 /home/passhport/.ssh/

# Generate keys if they don't exist
if [ ! -r "/home/passhport/.ssh/id_rsa" ]
then
  echo "Generating id_rsa key pair…"
  /usr/bin/ssh-keygen -t rsa -b 4096 -N "" -f "/home/passhport/.ssh/id_rsa"
fi

if [ ! -r "/home/passhport/.ssh/id_ecdsa" ]
then
  echo "Generating id_ecdsa key pair…"
  /usr/bin/ssh-keygen -t ecdsa -b 521 -N "" -f "/home/passhport/.ssh/id_ecdsa"
fi

if [ ! -r "/home/passhport/.ssh/id_ed25519" ]
then
  echo "Generating id_ed25519 key pair…"
  /usr/bin/ssh-keygen -t ed25519 -N "" -f "/home/passhport/.ssh/id_ed25519"
fi

##################
# SSHD HOST KEYS #
##################
if [ ! -r "/home/passhport/.sshd/ssh_host_dsa_key" ]
then
  ssh-keygen -q -N "" -t dsa -f "/home/passhport/.sshd/ssh_host_dsa_key"
fi
if [ ! -r "/home/passhport/.sshd/ssh_host_rsa_key" ]
then
  ssh-keygen -q -N "" -t rsa -b 4096 -f "/home/passhport/.sshd/ssh_host_rsa_key"
fi
if [ ! -r "/home/passhport/.sshd/ssh_host_ecdsa_key" ]
then
  ssh-keygen -q -N "" -t ecdsa -f "/home/passhport/.sshd/ssh_host_ecdsa_key"
fi
if [ ! -r "/home/passhport/.sshd/ssh_host_ed25519_key" ]
then
  ssh-keygen -q -N "" -t ed25519 -f "/home/passhport/.sshd/ssh_host_ed25519_key"
fi

##########################
# DataBase configuration #
##########################
if [ -n "${POSTGRES_CONNECTION_STRING}" ]
then
  sed -i -e "s#SQLALCHEMY_DATABASE_URI\s\+=.*#SQLALCHEMY_DATABASE_URI = ${POSTGRES_CONNECTION_STRING}#g" /etc/passhport/passhportd.ini
else
  echo 'Error : $POSTGRES_CONNECTION_STRING environment variable is not set.'
  exit 1
fi	
if [ ! -e "/home/passhport/var/app.db" ]
then
  echo "Passhportd database does not exist. Creating database…"
  if [ ! -e "/home/passhport/var" ]
  then
    mkdir "/home/passhport/var"
  fi
  ${PYTHON_ENV_RUNTIME} /home/passhport/passhport/passhportd/db_create.py
fi

if [ ! -e "/home/passhport/certs" ]
then
  echo "Certification directory does not exist. Creating them…"
  mkdir /home/passhport/certs
  chmod 700 /home/passhport/certs
fi

if [ ! -r "/home/passhport/certs/key.pem" ]
then
  echo "Generating passhportd web API key…"
  openssl genrsa -out "/home/passhport/certs/key.pem" 4096
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
  echo "DNS.3 = ${PASSHPORTD_HOSTNAME}" >> "/home/passhport/passhport/tools/confs/openssl-for-passhportd.cnf" 
  openssl req -new -key "/home/passhport/certs/key.pem" \
        -config "/home/passhport/passhport/tools/confs/openssl-for-passhportd.cnf" \
        -out "/home/passhport/certs/cert.pem" \
        -subj '/C=FR/ST=Ile De France/L=Ivry sur Seine/O=LibrIT/OU=DSI/CN=${PASSHPORTD_HOSTNAME}' \
        -x509 -days 365 -sha256\
        -extensions v3_req
fi

/usr/sbin/sshd -f /home/passhport/passhport/tools/confs/sshd_config

# Launch the passhportd in the virtualenv
"${PYTHON_ENV_RUNTIME}" /home/passhport/passhport/passhportd/passhportd

