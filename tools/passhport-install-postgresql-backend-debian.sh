#!/bin/bash
# From https://docs.passhport.org/en/latest/installation-and-configuration/use-postgresql-as-backend.html

echo '###################################'
echo '# PostgreSQL Backend installation #'
echo '###################################'
# install postgresql
echo "Installing postgresql"
apt -y install postgresql postgresql-server-dev-11

# As passhport user, install psycopg2 and psycopg2-binary:
echo "Install required python libs in virtual-env"
su - passhport -c '/home/passhport/passhport-run-env/bin/pip install psycopg2 psycopg2-binary'

# Create a passhport user in postgreSQL server, and the corresponding database
echo "Create passhport postgres user"
su - postgres -c 'createuser -D -S -R passhport'
echo "Create passhport database"
su - postgres -c 'createdb -O passhport "passhport"'

# New PostgreSQL user 'passhport' password
echo "Generating password"
PASSHPORT_POSTGRESQL_PASSWORD=$(< /dev/urandom tr -dc -- -_A-Z-a-z-0-9 | head -c${1:-32};echo;)

# Set new password
echo "Setting password of passhport user in PostgreQSL"
su - postgres -c "psql postgres -c \"ALTER USER \\\"passhport\\\" WITH PASSWORD '${PASSHPORT_POSTGRESQL_PASSWORD}'\""

# Change passhportd configuration
echo "Updating passhportd configuration"
sed -i -e "s#SQLALCHEMY_DATABASE_URI\s*=.*#SQLALCHEMY_DATABASE_URI        = postgresql://passhport:${PASSHPORT_POSTGRESQL_PASSWORD}@localhost/passhport#" '/etc/passhport/passhportd.ini'

# Init new database
echo "Initializing database (db_create)"
su - passhport -c '/home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/db_create.py'

# Restart passhportd
echo 'Restarting passhportd'
systemctl restart passhportd
sleep 5

# Adding localhost
echo 'Re-creating the PaSSHport target'
su - passhport -c 'passhport-admin target create root@localhost 127.0.0.1 --comment="Localhost target added during the PaSSHport installation process."'
