#!/bin/bash
# Create virtual env and install python modules
su - passhport -c 'virtualenv -p python3.4 passhport-run-env'
su - passhport -c '/home/passhport/passhport-run-env/bin/pip install flask flask_login flask_wtf requests configparser'

# Copy default passhweb conf file and remove debug
cp /home/passhport/passhweb/passhweb.ini /etc/passhport/passhweb.ini
sed -i -e 's/^DEBUG\s*=.*/DEBUG = false/g' '/etc/passhport/passhweb.ini'

# Install apache2 and wsgi for python3
yum install -y httpd mod_wsgi

# Copy wsgi configuration file to apache2 mods directory
cp /home/passhport/passhweb/tools/apache.conf /etc/httpd/conf.d/passhweb.conf
sed -i -e 's#\(\s*ErrorLog\)\s\+.*#\1\t/var/log/httpd/passhweb-error.log#' /etc/httpd/conf.d/passhweb.conf
sed -i -e 's#\(\s*CustomLog\)\s\+.*#\1\t/var/log/httpd/passhweb-access.log combined#' /etc/httpd/conf.d/passhweb.conf

echo "Installing WSGI python 3 apache module"
yum install -y httpd-devel python34-pip
pip3.4 install mod-wsgi
mod_wsgi-express install-module > /etc/httpd/conf.modules.d/02-wsgi.conf
yum autoremove -y httpd-devel


systemctl restart httpd
echo "Apache has been restarted."

echo "Add firewalld rule"
firewall-cmd --zone=public --add-port=80/tcp

echo "Fixing directory perm so httpd can access to wsgi file"
chmod o=x /home/passhport/

systemctl restart httpd

echo "Now go to http://SERVER-IP/fusiondirectory"
echo "Press Enter when ready"
read

su - passhport -c "virtualenv -p python3 /home/passhport/passhport-run-env"

su - passhport -c "/home/passhport/passhport-run-env/bin/pip install flask flask_login flask_wtf requests"


