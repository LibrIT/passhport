#!/bin/bash -e 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# Should we run as interactive mode ? (-s non interactive mode)
INTERACTIVE=1
PASSHPORTDO="su - passhport -c"
POSTGRESDO="su - postgres -c"
POSTGRESPASS=$(cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 22) # or force it
RED='\033[0;31m'
GREEN='\033[0;32m'
LGREEN='\033[1;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color


purge()
{
	if [ ${INTERACTIVE} -eq 1 ]
	then
		echo -e "${RED}Be warned that ALL your installation will be erased. You will LOST DATA. ALL appache conf and postgresql databases will be erased by apt... this function should be used by devs only${NC}"
		echo -e "${RED}Last chance! Type yes if you accept to lose data and configuration, or exit with 'CTRL+C' :${NC}"
	read ANSWER;
else
	ANSWER='yes'
fi

while [ "${ANSWER}" != 'yes' ]
do
	echo 'Please type excatly "yes" or exit by pressing "CTRL+C".'
	read ANSWER
done

echo -e "${BLUE}Purge database/apache and dependances… ${NC}"
apt purge -f python3-pip python3-venv git openssl  libpython3-dev postgresql apache2 libapache2-mod-wsgi-py3 libpq-dev
echo

echo -e "${BLUE}Remove directories${NC}"
rm -rf /etc/passhport/ /var/log/passhport/ /home/passhport /etc/bash_completion.d/passhport-admin
rm -rf /usr/local/bin/passhport-admin

echo -e "${BLUE}Remove user${NC}"
userdel  passhport
}


install()
{
echo -e "This script will install ${GREEN}PaSSHport${NC} on a fresh Debian 11 (Bullseye)."
echo 
echo 'This script will:'
echo '- install PaSSHport Python dependancies'
echo '- install a venv (virtualenv for PaSSHport dependancies execution)'
echo '- add a "passhport" system user'
echo '- add a local postgresql installation and link passhport to it'
echo '- add a local apache with wsgi to run passhport service'
echo '- create various directories to store conf, log and databases'
echo
echo -e "${RED}Be warned that this script needs to be run on a fresh system, no guarantees here"
echo 
echo -e "${BLUE}If you want to ${RED}remove${BLUE} passhportd from this system, run this script with option '-p'.${NC}"
echo ''

if [ ${INTERACTIVE} -eq 1 ]
then
	echo -e "${BLUE}Once you read and understood the above lines, you may proceed by typing"
	echo -e "'${GREEN}yes${BLUE}', or exit by the famous '${RED}CTRL+C${BLUE}' :${NC}"
	read ANSWER;
else
	ANSWER='yes'
fi

while [ "${ANSWER}" != 'yes' ]
do
	echo -e "${BLUE}Please type excatly "${GREEN}yes${BLUE}" or exit by pressing '${RED}CTRL+C${BLUE}'.${NC}"
	read ANSWER
done

################################################## GENERAL ##################################################
# Install dependances
echo -e "${BLUE}Installing dependances via APT… ${NC}"
apt update
apt install -y python3-pip python3-venv git openssl  libpython3-dev postgresql apache2 libapache2-mod-wsgi-py3 libpq-dev
echo

# Passhport user creation
echo -e "${BLUE}Create passhport user...${NC}"
/usr/sbin/useradd --home-dir /home/passhport --shell /bin/bash --create-home passhport
#in case the user exists but the homedir didn't... (happens if the purge is launched from a passhport ssh session)
[ ! -e "/home/passhport/" ] && mkdir /home/passhport && chown passhport:passhport /home/passhport
echo

# Download passhport code
echo -e "${BLUE}Cloning passhport git from github...${NC}"
if [ ! -z "${GITBRANCH}" ]
then
	${PASSHPORTDO} "git clone --single-branch --branch ${GITBRANCH} https://github.com/LibrIT/passhport.git"
else
	${PASSHPORTDO} "git clone https://github.com/LibrIT/passhport.git"
fi
echo 

# Configure initial system and create env
echo -e "${BLUE}Create conf and log directories...${NC}"
mkdir -p /var/log/passhport/
chown passhport:passhport /var/log/passhport/
mkdir -p /etc/passhport
cp /home/passhport/passhport/passhportd/passhportd.ini /etc/passhport/.
cp /home/passhport/passhport/passhport/passhport.ini /etc/passhport/.
cp /home/passhport/passhport/passhport-admin/passhport-admin.ini /etc/passhport/.
cp /home/passhport/passhport/passhportd/passhportd.ini /etc/passhport/.
sed -i -e 's#SQLALCHEMY_DATABASE_DIR\s*=.*#SQLALCHEMY_DATABASE_DIR        = /var/lib/passhport/#' /etc/passhport/passhportd.ini
sed -i -e 's#LISTENING_IP\s*=.*#LISTENING_IP = 0.0.0.0#' /etc/passhport/passhportd.ini
sed -i -e 's#SQLALCHEMY_MIGRATE_REPO\s*=.*#SQLALCHEMY_MIGRATE_REPO        = /var/lib/passhport/db_repository#' /etc/passhport/passhportd.ini
sed -i -e "s#SQLALCHEMY_DATABASE_URI\s*=.*#SQLALCHEMY_DATABASE_URI        = postgresql://passhport:${POSTGRESPASS}@localhost/passhport#" /etc/passhport/passhportd.ini
sed -i -e "s#PASSHPORTD_HOSTNAME\s*=.*#PASSHPORTD_HOSTNAME = localhost#" /etc/passhport/passhport-admin.ini
sed -i -e "s#PASSHPORTD_HOSTNAME\s*=.*#PASSHPORTD_HOSTNAME = localhost#" /etc/passhport/passhport.ini
echo

# Prepare venv
echo -e "${BLUE}Installing mandatory packages in a new python3 venv...${NC}"
${PASSHPORTDO} "python3 -m venv passhport-run-env"
${PASSHPORTDO} "/home/passhport/passhport-run-env/bin/pip install -r /home/passhport/passhport/requirements.txt"
${PASSHPORTDO} "/home/passhport/passhport-run-env/bin/pip install psycopg2 psycopg2-binary"
echo

# Generate keys to be put on targes
echo -e "${BLUE}Generating PaSSHport Legacy RSA (avoid to use it), legacy ecdsa (avoid to use it) and the modern ed25519 keys you will have to put on target…${NC}"
${PASSHPORTDO} '/usr/bin/ssh-keygen -t rsa -b 4096 -N "" -f "/home/passhport/.ssh/id_legacy_rsa"'
${PASSHPORTDO} '/usr/bin/ssh-keygen -t ecdsa -b 521 -N "" -f "/home/passhport/.ssh/id_legacy_ecdsa"'
${PASSHPORTDO} '/usr/bin/ssh-keygen -t ed25519 -b 521 -N "" -f "/home/passhport/.ssh/id_ed25519"'
echo

# Bash completion and binaries paths
echo -e "${BLUE}Add passhport-admin in the pash and activate completion…${NC}"
if [ ! -d "/etc/bash_completion.d/" ]
then
	mkdir "/etc/bash_completion.d/"
fi
cp /home/passhport/passhport/tools/confs/passhport-admin.bash_completion /etc/bash_completion.d/passhport-admin
. /etc/bash_completion.d/passhport-admin
ln -s /home/passhport/passhport/tools/bin/passhport-admin.sh /usr/local/bin/passhport-admin
echo

# SSL Certificates time! 
echo -e "${BLUE}Creating some http certificates for the passhportd service${NC}"
${PASSHPORTDO} "mkdir /home/passhport/certs"
${PASSHPORTDO} "chmod 700 /home/passhport/certs"
${PASSHPORTDO} "openssl genrsa -out "/home/passhport/certs/key.pem" 4096"
sed -i -e "s#^\(DNS.*\s*=\s*\)TO_CHANGE#\1`hostname -f`#g" /home/passhport/passhport/tools/confs/openssl-for-passhportd.cnf 
openssl req -new -key "/home/passhport/certs/key.pem" \
	-config "/home/passhport/passhport/tools/confs/openssl-for-passhportd.cnf" \
	-out "/home/passhport/certs/cert.pem" \
	-subj "/C=FR/ST=Ile De France/L=Ivry sur Seine/O=LibrIT/OU=DSI/CN=passhport.librit.fr" \
	-x509 \
	-days 365 \
	-sha256 \
	-extensions v3_req
echo


################################################## DATABASE ##################################################

# Postgresql
echo -e "${BLUE}Configure access to postgresql database and initialize it...${NC}"
${POSTGRESDO} "createuser -D -S -R passhport && createdb -O passhport 'passhport'"
${POSTGRESDO} "psql -U postgres -d passhport -c \"alter user passhport with password '${POSTGRESPASS}';\""
${PASSHPORTDO} "/home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/db_create.py"
echo


################################################## APACHE/WSGI ##################################################
echo -e "${BLUE}Create apache2 configuration for passhport and restart apache2...${NC}"
echo "Listen 5000
<VirtualHost *:5000>
    ServerName passhport

    SSLEngine               on
    SSLCertificateFile      /home/passhport/certs/cert.pem
    SSLCertificatekeyFile   /home/passhport/certs/key.pem

    WSGIDaemonProcess passhport user=passhport group=passhport threads=5  python-home=/home/passhport/passhport-run-env/
    WSGIScriptAlias / /home/passhport/passhport/tools/passhportd.wsgi
    <Directory /home/passhport/ >
        WSGIProcessGroup passhport
        WSGIApplicationGroup %{GLOBAL}
        # passhportd don't provides authentication, please filter by IP
        Require ip 127.0.0.1/8 ::1/128
    </Directory>
</VirtualHost>" > /etc/apache2/sites-available/passhport.conf

systemctl restart apache2
# Sleep 2 seconds so apache has enough time to start
sleep 2
echo


################################################## INITIAL CONF ##################################################
echo -e "${BLUE}Adding root@localhost target…${NC}"
[ ! -d "/root/.ssh" ] && mkdir "/root/.ssh" && chmod 700 "/root/.ssh"
cat "/home/passhport/.ssh/id_ed25519.pub" >> "/root/.ssh/authorized_keys"
${PASSHPORTDO} 'passhport-admin target create root@localhost 127.0.0.1 --comment="Localhost target added during the PaSSHport installation process."'
if [ ${INTERACTIVE} -eq 1 ]
then
	echo -e "${GREEN}Do you want to add your first user now ? Y/n${NC}"
	read DO_CREATE_USER
else
	DO_CREATE_USER='n'
fi
while [ "${DO_CREATE_USER,,}" != "y" ] && [ ! -z "${DO_CREATE_USER}" ] && [ "${DO_CREATE_USER,,}" != "n" ]
do
	echo -e "${GREEN}Do you want to add your first user now ? Y/n${NC}"
	read DO_CREATE_USER
done
if [ "${DO_CREATE_USER,,}" == "y" ] || [ -z "${DO_CREATE_USER}" ]
then
	echo -e "${LGREEN}Remember : no space in the user name!${NC}"
	${PASSHPORTDO} "passhport-admin user create"
	echo -e "${LGREEN}Do you want to link this user to the target root@localhost ? Y/n${NC}"
	read DO_LINK_USER
	while [ "${DO_LINK_USER,,}" != "y" ] && [ ! -z "${DO_LINK_USER}" ] && [ "${DO_LINK_USER,,}" != "n" ]
	do
		echo -e "${LGREEN}Do you want to link this user to the target root@localhost ? Y/n${NC}"
		read DO_LINK_USER
	done
	if [ "${DO_LINK_USER,,}" == "y" ] || [ -z "${DO_LINK_USER}" ]
	then
		FIRST_USER=`${PASSHPORTDO} "passhport-admin user list"`
		${PASSHPORTDO} "passhport-admin target adduser ${FIRST_USER} root@localhost"
	fi
fi
echo

echo -e "${BLUE}PaSSHport should be installed on your system.${NC}"
echo 'We test it with this command: curl -s --insecure https://localhost:5000'
echo -ne "${GREEN}"
curl -s --insecure https://localhost:5000

if [ ${INTERACTIVE} -eq 1 ]
then
	echo -e "${BLUE}If you created your first user, you can connect to PaSSHport${NC}"
	echo -e "${BLUE}using 'ssh -i the_key_you_used passhport@PASSHPORT_HOST'${NC}"
fi

echo 'Installation is now done.'
}


##### MAIN #####
while getopts ":sbpe:" OPTION
do
	case ${OPTION} in
		s) 
			INTERACTIVE=0
			;;
		b) 
			GITBRANCH=${OPTARG}
			;;
		p)
			purge 
			exit 0
			;;
		*) 
			echo "Unknown option, exiting..."
			exit 1
			;;   # DEFAULT
	esac
done

install


