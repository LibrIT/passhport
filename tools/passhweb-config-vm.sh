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

# First change secret in passhweb.ini
sed -i "s/^SECRET.*/SECRET = $(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 20 | head -n 1)/" /etc/passhport/passhweb.ini

# Commit on vm mode saying it's the first launch to activate config page
touch /home/passhport/passhport/.firstlaunch

# 

systemctl restart apache2
