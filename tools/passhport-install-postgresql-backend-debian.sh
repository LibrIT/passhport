#!/bin/bash
# From https://docs.passhport.org/en/latest/installation-and-configuration/use-postgresql-as-backend.html

# install postgresql
apt -y install postgresql postgresql-server-dev-11

# As passhport user, install psycopg2 and psycopg2-binary:
su - passhport -c '/home/passhport/passhport-run-env/bin/pip install psycopg2 psycopg2-binary'

# Create a passhport user in you postgreSQL server 
su - postgres -c 'createuser -D -S -R passhport && createdb -O passhport "passhport"'

# New PostgreSQL user 'passhport' password 
PASSHPORT_POSTGRESQL_PASSWORD=$(< /dev/urandom tr -dc -- -_A-Z-a-z-0-9 | head -c${1:-32};echo;)

# Set new password
su - postgres -c "psql postgres -c \"ALTER USER \\\"passhport\\\" WITH PASSWORD '${PASSHPORT_POSTGRESQL_PASSWORD}'\""

# Change passhportd configuration
sed -i -e "s#SQLALCHEMY_DATABASE_URI\s*=.*#SQLALCHEMY_DATABASE_URI        = postgresql://passhport:${PASSHPORT_POSTGRESQL_PASSWORD}@localhost/passhport#" '/etc/passhport/passhportd.ini'

# Init new database
su - passhport -c '/home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/db_create.py'

# Restart passhportd
systemctl restart passhportd

# Adding localhost
su - passhport -c 'passhport-admin target create root@localhost 127.0.0.1 --comment="Localhost target added during the PaSSHport installation process."'
