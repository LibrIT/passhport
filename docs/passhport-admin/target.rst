target
=============================

Usages :

.. code-block:: none

  passhport-admin target list
  passhport-admin target search [<pattern>]
  passhport-admin target checkaccess [<pattern>]
  passhport-admin target show [<name>]
  passhport-admin target create [((<name> <hostname>) [--login=<login>] [--type=<ssh>] [--comment=<comment>] [--sshoptions=<sshoptions>] [--port=<port>])]
  passhport-admin target edit [(<name> [--newname=<name>] [--newhostname=<hostname>] [--newlogin=<login>] [--newcomment=<comment>] [--newsshoptions=<sshoptions>] [--newport=<port>])]
  passhport-admin target (adduser | rmuser) [(<username> <targetname>)]
  passhport-admin target (addusergroup | rmusergroup) [(<usergroupname> <targetname>)]
  passhport-admin target delete [([-f | --force] <name>)]

list
-----

`passhport-admin target list` show all the configured targets.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin target list
  srv1.compagny.com
  srv2.compagny.com
  srv3.compagny.com
  websrv.ext.client.com
  webbackend.ext.client.com
  admin@bastion:~$

search
---------

`passhport-admin target search [<PATTERN>]` searches in the target list for all targets that correspond to the given pattern.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin target search web
  websrv.ext.client.com
  webbackend.ext.client.com
  admin@bastion:~$

If no pattern is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin target search
  Pattern: web
  websrv.ext.client.com
  webbackend.ext.client.com
  admin@bastion:~$

checkaccess
-------------

`passhport-admin target checkaccess [<PATTERN>]` verifies that PaSSHport has access to the all targets that correspond to the given pattern.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin target checkaccess web
  OK:    132.123.45.67   websrv.ext.client.com
  OK:    132.234.56.78   webbackend.ext.client.com
  admin@bastion:~$

If no pattern is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin target checkaccess
  Pattern: web
  OK:    132.123.45.67   websrv.ext.client.com
  OK:    132.234.56.78   webbackend.ext.client.com
  admin@bastion:~$

show
-------

`passhport-admin target show <NAME>` shows informations about the target <NAME>.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin target show websrv.ext.client.com
  Name: websrv.ext.client.com
  Hostname: 132.123.45.67
  Server Type : ssh
  Login: root
  Port: 22
  SSH options:
  Comment: 
  Attached users: 
  Usergroup list: 
  Users who can access this target: admin1@compagny.com admin2@compagny.com
  All usergroups: 
  Member of the following targetgroups: all-targets
  admin@bastion:~$

If no pattern is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin target show
  Name: websrv.ext.client.com
  Name: websrv.ext.client.com
  Hostname: 132.123.45.67
  Server Type : ssh
  Login: root
  Port: 22
  SSH options:
  Comment: 
  Attached users: 
  Usergroup list: 
  Users who can access this target: admin1@compagny.com admin2@compagny.com
  All usergroups: 
  Member of the following targetgroups: all-targets
  admin@bastion:~$

create
----------

`passhport-admin target create [((<name> <hostname>) [--login=<login>] [--type=<ssh>] [--comment=<comment>] [--sshoptions=<sshoptions>] [--port=<port>])]` creates a new target.

================== ==========================================================================
Argument           Description
================== ==========================================================================
<name>             Name of the target to create

hostname           Hostname or IP of the target

--login            Login to use when accessing the target (optional)

--type             The type of the target (for the commercial version only). 
                   It can be `ssh`, `postgresql`, `mysql`, `oracle`.<br/>
                   This is used to know which hook to launch, depending on the server<br/>
                   type. If type is something else than `ssh`, the server won't be <br/> 
                   accessible via SSH. If the target is a PostGreSQL server and you <br/>
                   want to lauch the corresponding hook (usually a proxy to log user <br/>
                   actions, use `postgresql` type). Same explanations for `mysql` and <br/>
                   `oracle`.<br/>
                   Use the default `ssh`, unless you have the commercial version.<br/>

--comment          Comment concerning the target (optional)

--sshoptions       SSH options to use when connecting to the target (optional)

--port             SSH port to use when connecting to the target (optional)
================== ==========================================================================

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target create firewall.compagny.com 87.65.43.219 --login=root --comment="Client 1 web server number 1"
  OK: "firewall.compagny.com" -> created
  admin@bastion:~#

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target create 
  Name: firewall2.compagny.com
  Hostname: 87.65.43.220
  Type (default is ssh):
  Login (default is root):
  Port: 22
  SSH Options: 
  Comment: Client 1 FireWall 2 (Cisco)
  OK: "firewall1.compagny.com" -> created
  admin@bastion:~#

Once the target is created, you should add a passhport ssh public key to the target and use "checkaccess" to verify everything is ok.

edit
-----------

`passhport-admin target edit [(<name> [--newname=<name>] [--newhostname=<hostname>] [--newtype=<ssh>] [--newlogin=<login>] [--newcomment=<comment>] [--newsshoptions=<sshoptions>] [--newport=<port>])]` edits an existing target.

================== ==========================================================================
Argument           Description
================== ==========================================================================
<name>             Name of the target to edit

--newname          New name of the target if you want to rename it (optional)

--newhostname      New hostname/IP of the target (optional)

--newtype          The type of the target (for the commercial version only). 
                   It can be `ssh`, `postgresql`, `mysql`, `oracle`.<br/>
                   This is used to know which hook to launch, depending on the server<br/>
                   type. If type is something else than `ssh`, the server won't be <br/> 
                   accessible via SSH. If the target is a PostGreSQL server and you <br/>
                   want to lauch the corresponding hook (usually a proxy to log user <br/>
                   actions, use `postgresql` type). Same explanations for `mysql` and <br/>
                   `oracle`.<br/>
                   Use the default `ssh`, unless you have the commercial version.<br/>

--newlogin         New login to use when accessing the target (optional)

--newcomment       New comment concerning the target (optional)

--newsshoptions    New SSH options to use when connecting to the target (optional)

--newport          New SSH port to use when connecting to the target (optional)
================== ==========================================================================

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target edit firewall.compagny.com --newname=firewall1.compagny.com --newcomment="Client 1 FireWall 1 (Cisco)" --newlogin="admin"
  OK: "firewall.compagny.com" -> edited
  admin@bastion:~#

If no argument is given, user enters in interactive mode. It firsts shows all parameters of the target, then displays each parameters for a change. User can keep any previous configured parameter, just by typing "Enter". They only exception is the comment. If user wants to remove the comment, he just type "Enter", and will then be asked if the original comment should be removed or not.

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target edit 
  Name of the target you want to modify: firewall2.compagny.com
  Name: firewall2.compagny.com
  Hostname: 87.65.43.220
  Server Type : ssh
  Login: root
  Port: 22
  SSH options: 
  Comment: Client 1 FireWall 2 (Cisco)
  Attached users: 
  Usergroup list: 
  Users who can access this target: 
  All usergroups: 
  Member of the following targetgroups: 
  New name: 
  New hostname: 
  New Login: admin
  New port: 
  New SSH options: 
  New comment: 
  Remove original comment? [y/N]N
  OK: "firewall2.compagny.com" -> edited
  admin@bastion:~# 

As you can see above, we only changed the "New Login" entry. If an entry is simply replied with "enter", it keeps the previous value.

adduser
-----------

`passhport-admin target adduser [(<username> <targetname>)]` connects a target directly to a user.

================== ===================================================================
Argument           Description
================== ===================================================================
<username>         Name of the user to connect to the target

<targetname>       Name of the target on which to connect the user
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target adduser admin1@compagny.com firewall1.compagny.com 
  OK: "admin1@compagny.com" added to "firewall1.compagny.com"
  admin@bastion:~#

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target adduser
  Username: admin2@compagny.com
  Targetname: firewall2.compagny.com
  OK: "admin2@compagny.com" added to "firewall2.compagny.com"
  admin@bastion:~#

rmuser
-----------

`passhport-admin target rmuser [(<username> <targetname>)]` deletes the direct connection between a target and a user.

================== ===================================================================
Argument           Description
================== ===================================================================
<username>         Name of the user to disconnect to the target

<targetname>       Name of the target on which to disconnect the user
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target rmuser admin1@compagny.com firewall1.compagny.com
  OK: "admin1@compagny.com" removed from "firewall1.compagny.com"
  admin@bastion:~#

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target rmuser 
  Username: admin2@compagny.com
  Targetname: firewall2.compagny.com
  OK: "admin2@compagny.com" removed from "firewall2.compagny.com"
  admin@bastion:~# 

addusergroup
-------------

`passhport-admin target addusergroup [(<usergroupname> <targetname>)]` connects a target directly to a usergroup.

================== ===================================================================
Argument           Description
================== ===================================================================
<usergroupname>    Name of the usergroup to connect to the target

<targetname>       Name of the target on which to connect the usergroup
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target addusergroup firewall-admins firewall1.compagny.com 
  OK: "firewall-admins" added to "firewall1.compagny.com"
  admin@bastion:~#

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target addusergroup
  Usergroupname: firewall-admins
  Targetname: firewall2.compagny.com
  OK: "firewall-admins" added to "firewall2.compagny.com"
  admin@bastion:~#

rmusergroup
-----------

`passhport-admin target delusergroup [(<usergroupname> <targetname>)]` delete the connection between a target and a usergroup.

================== ===================================================================
Argument           Description
================== ===================================================================
<usergroupname>    Name of the usergroup to disconnect to the target

<targetname>       Name of the target on which to disconnect the usergroup
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target addusergroup firewall-admins firewall1.compagny.com 
  OK: "firewall-admins" added to "firewall1.compagny.com"
  admin@bastion:~#

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target addusergroup
  Usergroupname: firewall-admins
  Targetname: firewall2.compagny.com
  OK: "firewall-admins" added to "firewall2.compagny.com"
  admin@bastion:~#

delete
-----------

`passhport-admin target delete [([-f | --force] <name>)]` delete a target.

================== ===================================================================
Argument           Description
================== ===================================================================
<name>             Name of the target to delete

-f or --force      If used, user won't be prompt for confirmation
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target delete firewall1.compagny.com 
  Name: firewall1.compagny.com
  Hostname: firewall1.compagny.com
  Server Type : ssh
  Login: admin
  Port: 22
  SSH options: 
  Comment: Client 1 FireWall 1 (Cisco)
  Attached users: 
  Usergroup list: firewall-admins
  Users who can access this target: 
  All usergroups: firewall-admins
  Member of the following targetgroups: 
  Are you sure you want to delete firewall1.compagny.com? [y/N] y
  OK: "firewall1.compagny.com" -> deleted
  admin@bastion:~#

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~# passhport-admin target delete
  Name: firewall2.compagny.com
  Name: firewall2.compagny.com
  Hostname: 87.65.43.220
  Server Type : ssh
  Login: admin
  Port: 22
  SSH options: 
  Comment: Client 1 FireWall 2 (Cisco)
  Attached users: 
  Usergroup list: firewall-admins network-admins
  Users who can access this target: 
  All usergroups: firewall-admins network-admins
  Member of the following targetgroups: 
  Are you sure you want to delete firewall2.compagny.com? [y/N] y
  OK: "firewall2.compagny.com" -> deleted
  admin@bastion:~# 
