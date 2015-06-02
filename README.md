passhport
=========

Your main adminsys goes away of your company. Are you sure all his ssh access are revoked? What about the interns? The consultants?... Let's fix this.

Requirements:
-------------
 * All users have to provide their public ssh key.
 * ssh-agent on client

Goals:
------
 * Manage users on a centralized server technology independant (no ldap)
 * Manage users as "roles" (or groups): adminsys, devops, supervision team...
 * Manage servers and groups of servers
 * Limit servers interractions (limitation to some commands)
 * Provide a connexions history
 * Provide command and actions history (by users)

Done so far: 
-------------
 * Server API Caneva (REST urls ready to answer with Flask)
 * User and target management via the API
 * Server database initialization (no data)
 * Client interface with interactive console
 
Used technologies:
------------------
 * OpenSSH
 * Python
 * Docopt
 * Flask
 * Alchemy
 * Flask-Alchemy
 * Alchemy-migration

