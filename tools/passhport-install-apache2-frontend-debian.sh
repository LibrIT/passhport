#! /bin/bash

echo '##################################'
echo '# APACHE2 FRONT-END INSTALLATION #'
echo '##################################'

# Install Apache2
echo 'Installing apache2 ans mod-wsgi for python3'
apt -y install apache2 libapache2-mod-wsgi-py3

# Create vhost file
echo 'Create passhportd configuration file for apache2'
cat <<EOF > /etc/apache2/sites-available/passhportd.conf
Listen 5000
<VirtualHost *:5000>
	ServerName passhport

	SSLEngine		on
	SSLCertificateFile	/home/passhport/certs/cert.pem
	SSLCertificatekeyFile	/home/passhport/certs/key.pem

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

echo 'Disabling default apache2 site'
a2dissite 000-default

echo 'Enabling ssl module for apache2'
a2enmod ssl

echo 'Activate passhportd configuration'
a2ensite passhportd.conf

echo 'Stop current passhportd'
systemctl stop passhportd
systemctl disable passhportd

echo ""
rm /etc/systemd/system/passhportd.service

echo 'Restarting apache2'
systemctl restart apache2 || journalctl -xeu apache2
systemctl enable apache2
