PaSSHport
=========
[![Documentation Status](https://readthedocs.org/projects/passhport/badge/?version=latest)](http://docs.passhport.org/en/latest/?badge=latest)

Your main adminsys goes away of your company. Are you sure all his ssh access are revoked? What about the interns? The consultants?... Let's fix this!

Documentation (installation, usage):
-------------------------------------
https://docs.passhport.org

Requirements:
-------------
 * Standard OpenSSH server
 * Standard OpenSSH client

Goals:
------
 * Manage users on a centralized server technology independant (no ldap)
 * Manage users as "roles" (or groups): adminsys, devops, supervision team...
 * Manage servers and groups of servers
 * Provide a connexions history
 * Provide command and actions history (by users)
 
 Test the 5 minutes Debian installation :
 ```
 bash <(curl -s https://raw.githubusercontent.com/librit/passhport/master/tools/passhport-install-script-debian.sh)
 ```
