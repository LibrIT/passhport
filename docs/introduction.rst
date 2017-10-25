Introduction to PaSSHport
=========================

PaSSHport is a software that allows you to control the SSH access of your IT components : Linux/Unix servers, network switchs, routers, WiFi access points, and any appliances that is accessed by SSH.
In three words : who accesses what ?

PaSSHport has been written with the following in mind :

* Similar to `SSHgate <https://github.com/Tauop/sshGate>`_
* Two main objects : targets and users (we'll see below what are those)
* Objects can be grouped : targetgroups and usergroups
* Record all sessions of users
* Can be fully configure and used from the command line interface
* Can do Secured Copy (scp)
* REST API based communication between components so that it can be easily integrated in an automated IT environment
* Use only OpenSource technologies

Please read below to understand the main components, and how they work together.

Components
----------
PaSSHport project is composed with 3 main programs :

* passhportd : the daemon that verify access rights, and store configuration
* passhport : the script that receive the connection (it does NOT replace the SSH server). Think of it has the shell a user falls into when connecting to a PaSSHport gateway
* passhport-admin : the script that is used to configure passhportd. SysAdmins will use it to add a *user*, a *target*, a *usergroup*, a *targetgroup*, and combine those to configure accesses

.. image:: images/Composants_PaSSHport_EN.png

Now let's go to the installation process…
