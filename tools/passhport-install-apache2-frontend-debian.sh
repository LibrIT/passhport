#! /bin/bash

# Install Apache2
apt -y install apache2 libapache2-mod-wsgi-py3

# Create vhost file
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


a2dissite 000-default
a2enmod ssl
a2ensite passhportd.conf

systemctl restart apache2
