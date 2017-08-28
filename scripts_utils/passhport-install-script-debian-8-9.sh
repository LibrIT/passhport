#!/bin/bash -e 
echo 'Hi there ! Please read carefully the following (not long)'.
echo 'This script will attempt to install PaSSHport on this system.'
echo 'This script works on Debian 8 (Jessy) and Debian 9 (Stretch).'
echo "It may also work on Debian 7, but it hasn't been tested."
echo ''
echo 'What this script will do to your existing system:'
echo '- install "python3-pip", "git" and "openssl" packages.'
echo '- update PIP via pip3 script, installed previously'
echo '- install virtualenv via pip3 script'
echo '- add a "passhport" system user'
echo '- create an "/etc/passhport" directory'
echo '- create a "/var/lib/passhport" directory'
echo '- create a "/var/log/passhport" directory'
echo ''
echo 'The remaining process will only create and/or modify files and'
echo 'directories WITHIN the directories mentionned above, so which includes:'
echo '- /home/passhport'
echo '- /etc/passhport'
echo '- /var/lib/passhport'
echo '- /var/log/passhport'
echo ''
echo 'If you want to remove passhportd from this system, run the following,'
echo 'as root:'
echo 'userdel passhport'
echo 'rm -rf /home/passhport'
echo 'rm -rf /etc/passhport'
echo 'rm -rf /var/lib/passhport'
echo 'rm -rf /var/log/passhport'
echo 'rm /usr/bin/passhport-admin'
echo 'rm /usr/sbin/passhportd'
echo 'You may also remove virtualenv that has been installed by pip3 :'
echo '# pip3 uninstall virtualenv'
echo "Finally you may also purge the following packages if you don't need them"
echo 'anymore:'
echo 'python3-pip git openssl (# apt purge python3-pip git openssl)'
echo ''
echo 'Once you read and understood the above lines, you may proceed by typing'
echo '"yes", or exit by the famous "CTRL+C" :'
read ANSWER;

while [ "${ANSWER}" != 'yes' ]
do
	echo 'Please type excatly "yes" or exit by pressing "CTRL+C".'
	read ANSWER
done

echo '##############################################################'
echo '# Updating repos…'
echo '##############################################################'
apt update
echo '##############################################################'
echo '# Installing python3-pip, git and openssl package…'
echo '##############################################################'
apt install -y python3-pip git openssl
echo '##############################################################'
echo '# Updating pip…'
echo '##############################################################'
pip3 install -U pip 
echo '##############################################################'
echo '# Installing virtualenv with pip…'
echo '##############################################################'
pip3 install virtualenv
echo '##############################################################'
echo '# Creating "passhport" system user'
echo '##############################################################'
useradd --home-dir /home/passhport --shell /bin/bash --create-home passhport
echo '##############################################################'
echo '# Creating the virtual-env for passhport…'
echo '##############################################################'
su - passhport -c "virtualenv -p python3 passhport-run-env"
echo '##############################################################'
echo '# Installing mandatory packages in the virtual environment…'
echo '##############################################################'
su - passhport -c "/home/passhport/passhport-run-env/bin/pip install pymysql sqlalchemy-migrate flask-migrate requests docopt configparser tabulate"
echo '##############################################################'
echo '# Cloning passhport git from github'
echo '##############################################################'
su - passhport -c "git clone https://github.com/LibrIT/passhport.git"
echo '##############################################################'
echo '# Creating "/var/log/passhport" log directory'
echo '##############################################################'
mkdir -p /var/log/passhport/
chown passhport:passhport /var/log/passhport/
echo '##############################################################'
echo '# Creating "/etc/passhport" conf directory '
echo '##############################################################'
mkdir /etc/passhport
cp /home/passhport/passhport/passhportd/passhportd.ini /etc/passhport/.
cp /home/passhport/passhport/passhport/passhport.ini /etc/passhport/.
cp /home/passhport/passhport/passhport_admin/passhport-admin.ini /etc/passhport/.
cp /home/passhport/passhport/passhportd/passhportd.ini /etc/passhport/.
echo '##############################################################'
echo '# Generating PaSSHport RSA (4096b) and ecdsa (521b) keys…'
echo '##############################################################'
su - passhport -c '/usr/bin/ssh-keygen -t rsa -b 4096 -N "" -f "/home/passhport/.ssh/id_rsa"'
su - passhport -c '/usr/bin/ssh-keygen -t ecdsa -b 521 -N "" -f "/home/passhport/.ssh/id_ecdsa"'
echo '##############################################################'
echo '# Creating PaSSHport database directory…'
echo '##############################################################'
mkdir -p /var/lib/passhport
chown -R passhport:passhport /var/lib/passhport/
echo '##############################################################'
echo '# Editing PaSSHport conf files…'
echo '##############################################################'
sed -i -e 's#SQLALCHEMY_DATABASE_DIR\s*=.*#SQLALCHEMY_DATABASE_DIR        = /var/lib/passhport/#' /etc/passhport/passhportd.ini
sed -i -e 's#LISTENING_IP\s*=.*#LISTENING_IP = 0.0.0.0#' /etc/passhport/passhportd.ini
sed -i -e 's#SQLALCHEMY_MIGRATE_REPO\s*=.*#SQLALCHEMY_MIGRATE_REPO        = /var/lib/passhport/db_repository#' /etc/passhport/passhportd.ini
sed -i -e 's#SQLALCHEMY_DATABASE_URI\s*=.*#SQLALCHEMY_DATABASE_URI        = sqlite:////var/lib/passhport/app.db#' /etc/passhport/passhportd.ini
sed -i -e "s#PASSHPORTD_HOSTNAME\s*=.*#PASSHPORTD_HOSTNAME = `hostname -f`#" /etc/passhport/passhport-admin.ini
sed -i -e "s#PASSHPORTD_HOSTNAME\s*=.*#PASSHPORTD_HOSTNAME = `hostname -f`#" /etc/passhport/passhport.ini
echo '##############################################################'
echo '# Creating database for PaSSHport (SQLite)…'
echo '##############################################################'
su - passhport -c "/home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/db_create.py"
echo '##############################################################'
echo '# Creating symbolink links to binaries…'
echo '##############################################################'
ln -s /home/passhport/passhport/scripts_utils/passhport-admin_v0.sh /usr/bin/passhport-admin
ln -s /home/passhport/passhport/scripts_utils/launch_passhportd_v0.sh /usr/sbin/passhportd
echo '##############################################################'
echo '# Creating Web-API cert directory…'
echo '##############################################################'
su - passhport -c "mkdir /home/passhport/certs"
su - passhport -c "chmod 700 /home/passhport/certs"
echo '##############################################################'
echo '# Generating Web-API RSA key (4096b)'
echo '##############################################################'
su - passhport -c "openssl genrsa -out "/home/passhport/certs/key.pem" 4096"
echo '##############################################################'
echo '# Adding choosen IP to the certificate…'
echo '##############################################################'
sed -i -e "s#^\(DNS.*\s*=\s*\)TO_CHANGE#\1`hostname -f`#g" /home/passhport/passhport/scripts_utils/openssl-for-passhportd.cnf 
echo '##############################################################'
echo '# Generating Web-API certificate…'
echo '##############################################################'
openssl req -new -key "/home/passhport/certs/key.pem" \
	-config "/home/passhport/passhport/scripts_utils/openssl-for-passhportd.cnf" \
	-out "/home/passhport/certs/cert.pem" \
	-subj "/C=FR/ST=Ile De France/L=Ivry sur Seine/O=LibrIT/OU=DSI/CN=passhport.librit.fr" \
	-x509 \
	-days 365 \
	-sha256 \
	-extensions v3_req
echo 'Do you wan to launch passhportd daemon ? (y/N)'
read ANSWER
if [ "${ANSWER}" == 'y' ] || [ "${ANSWER}" == 'yes' ]
then
	su - passhport -c "/home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/passhportd"
else
	echo 'To launch passhportd, run one of the following :'
	echo '- As root : # su - passhport -c "/home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/passhportd"'
	echo '- As passhport user : $ /home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/passhportd'
fi
