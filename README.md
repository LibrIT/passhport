passhport
=========

Your main adminsys goes away of your company. Are you sure all his ssh access are revoked? What about the interns? The consultant?... Let's fix this.

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
 * none

Used technologies:
------------------
 * OpenSSH
 * Python


