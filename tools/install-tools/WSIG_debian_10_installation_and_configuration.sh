#!/bin/bash
###############################################################
# WARNING : use with care on a running system. This script is #
#           made for new installations on Debian 10 - Buster. #
#                                                             #
# Goal : install apache, and mod WSGI for passhportd.         #
#                                                             #
###############################################################

if [[ "$EUID" -ne 0 ]]
then 
    echo "Please run as root"
    exit
fi

################
# INSTALL APACHE
yes | apt install -qqq apache2 libapache2-mod-wsgi-py3 wget


########################
# CONFIGURE APACHE VHOST
VHOSTCONF="/etc/apache2/sites-available/passhport.conf"

/bin/cat > ${VHOSTCONF} << EOF
Listen 5000
<VirtualHost *:5000>
    ServerName passhport

    SSLEngine               on
    SSLCertificateFile      /home/passhport/certs/cert.pem
    SSLCertificatekeyFile   /home/passhport/certs/key.pem

    WSGIDaemonProcess passhport user=passhport group=passhport threads=5
    WSGIScriptAlias / /home/passhport/passhport/tools/passhportd.wsgi
    <Directory /home/passhport/ >
        WSGIProcessGroup passhport
        WSGIApplicationGroup %{GLOBAL}
        # passhportd don't provides authentication, please filter by IP
        Require ip 127.0.0.1/8 ::1/128
    </Directory>
</VirtualHost>

EOF

#################################
# ENABLE APACHE MODULES AND VHOST
a2dissite 000-default
a2enmod ssl wsgi
a2ensite passhport.conf

################
# Restart apache
systemctl restart apache2

wget --no-check-certificate https://localhost:5000 -qO - 

echo
echo "WSIG installation done."
exit 0
