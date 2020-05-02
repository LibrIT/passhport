#!/bin/bash
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
# Create virtual env and install python modules
su - passhport -c 'virtualenv -p python3 passhport-run-env'
su - passhport -c '/home/passhport/passhport-run-env/bin/pip install flask flask_login flask_wtf requests'

# Copy default passhweb conf file and remove debug
sed -e 's/^DEBUG\s*=.*/DEBUG = false/g' '/home/passhport/passhport/passhweb/passhweb.ini' > '/etc/passhport/passhweb.ini'

# Install apache2 and wsgi for python3
apt install -y apache2 libapache2-mod-wsgi-py3

# Copy wsgi configuration file to apache2 mods directory
cp /home/passhport/passhport/tools/passhweb-apache.conf /etc/apache2/sites-available/passhweb.conf
a2ensite passhweb
systemctl restart apache2
