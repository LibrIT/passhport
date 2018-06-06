targetgroup
=============================

Usages :

.. code-block:: none
 
  passhport-admin targetgroup list
  passhport-admin targetgroup search [<pattern>]
  passhport-admin targetgroup show [<name>]
  passhport-admin targetgroup create [(<name> [--comment=<comment>])]
  passhport-admin targetgroup edit [(<name> [--newname=<name>] [--newcomment=<comment>])]
  passhport-admin targetgroup (adduser | rmuser) [(<username> <targetgroupname>)]
  passhport-admin targetgroup (addtarget | rmtarget) [(<targetname> <targetgroupname>)]
  passhport-admin targetgroup (addusergroup | rmusergroup) [(<usergroupname> <targetgroupname>)]
  passhport-admin targetgroup (addtargetgroup | rmtargetgroup) [(<subtargetgroupname> <targetgroupname>)]
  passhport-admin targetgroup delete [([-f | --force] <name>)]

list
-----

`passhport-admin targetgroup list` show all the configured targetgroups.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup list
  linux-servers
  network-appliances
  phone-appliance
  admin@bastion:~$

search
---------

`passhport-admin targetgroup search [<PATTERN>]` searches in the targetgroup list for all targetgroups that correspond to the given pattern.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup search appliance
  network-appliances
  phone-appliance
  admin@bastion:~$

If no pattern is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup search 
  Pattern: servers
  linux-servers
  admin@bastion:~$

show
-------

`passhport-admin targetgroup show <NAME>` shows informations about the targetgroup <NAME>.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup show linux-servers 
  Name: linux-servers
  Comment: 
  User list: 
  Target list: linux-7892 linux-7239 linux-1398
  Usergroup list: 
  Targetgroup list: 
  All users: 
  All targets: linux-1398 linux-7239 linux-7892
  All usergroups: 
  All targetgroups: 
  admin@bastion:~$

If no pattern is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup show
  Name: linux-servers
  Name: linux-servers
  Comment: 
  User list: 
  Target list: linux-7892 linux-7239 linux-1398
  Usergroup list: 
  Targetgroup list: 
  All users: 
  All targets: linux-1398 linux-7239 linux-7892
  All usergroups: 
  All targetgroups: 
  admin@bastion:~$ 

create
----------

`passhport-admin targetgroup create [(<name> [--comment=<comment>])]` creates a new targetgroup.

================== ===================================================================
Argument           Description
================== ===================================================================
<name>             Name of the targetgroup to create

--comment          Comment concerning the targetgroup (optional)
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup create linux-servers
  OK: "linux-servers" -> created
  admin@bastion:~$ 

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup create
  Name: phone-appliance
  Comment: Phones and IPBX appliances group.
  OK: "phone-appliance" -> created
  admin@bastion:~$ 

edit
-----------

`passhport-admin targetgroup edit [(<name> [--newname=<name>] [--newcomment=<comment>])]` edits an existing targetgroup.

================== ===================================================================
Argument           Description
================== ===================================================================
<name>             Name of the targetgroup to edit

--newname          New name of the targetgroup (optional)

--newcomment       New comment concerning the targetgroup (optional)
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup edit linux-servers --newcomment="Linux servers group."
  OK: "linux-servers" -> edited
  admin@bastion:~$

If no argument is given, user enters in interactive mode. It firsts shows all parameters of the target, then displays each parameters for a change. User can keep any previous configured parameter, just by typing "Enter". They only exception is the comment. If user wants to remove the comment, he just type "Enter", and will then be asked if the original comment should be removed or not.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup edit
  Name of the targetgroup you want to modify: network-appliances
  Name: network-appliances
  Comment: 
  User list: 
  Target list: 
  Usergroup list: 
  Targetgroup list: 
  All users: 
  All targets: 
  All usergroups: 
  All targetgroups: 
  New name: 
  New comment: Network appliance group.
  OK: "network-appliances" -> edited
  admin@bastion:~$

As you can see above, we only changed the "New comment" entry. If an entry is simply replied with "enter", it keeps the previous value.

adduser
-----------

`passhport-admin targetgroup adduser [(<username> <targetgroupname>)]` connects a targetgroup directly to a user.

================== ===================================================================
Argument           Description
================== ===================================================================
<username>         Name of the user to connect to the targetgroup

<targetname>       Name of the targetgroup on which to connect the user
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup adduser john@compagny.com linux-servers 
  OK: "john@compagny.com" added to "linux-servers"
  admin@bastion:~$

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup adduser
  Username: vincent@compagny.com
  Targetgroupname: network-appliances
  OK: "vincent@compagny.com" added to "network-appliances"
  admin@bastion:~$

rmuser
-----------

`passhport-admin targetgroup rmuser [(<username> <targetgroupname>)]` deletes the direct connection between a targetgroup and a user.

================== ===================================================================
Argument           Description
================== ===================================================================
<username>         Name of the user to disconnect to the targetgroup

<targetname>       Name of the targetgroup of which to disconnect the user
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup rmuser vincent@compagny.com network-appliances 
  OK: "vincent@compagny.com" removed from "network-appliances"
  admin@bastion:~$

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup rmuser
  Username: john@compagny.com
  Targetgroupname: linux-servers
  OK: "john@compagny.com" removed from "linux-servers"
  admin@bastion:~$

addusergroup
-------------

`passhport-admin targetgroup addusergroup [(<usergroupname> <targetgroupname>)]` connects a targetgroup directly to a usergroup.

================== ===================================================================
Argument           Description
================== ===================================================================
<usergroupname>    Name of the usergroup to connect to a targetgroup

<targetname>       Name of the targetgroup on which to connect the usergroup
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup addusergroup linux-admins linux-servers 
  OK: "linux-admins" added to "linux-servers"
  admin@bastion:~$ 

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup addusergroup 
  Usergroupname: network-admins
  Targetgroupname: network-appliances
  OK: "network-admins" added to "network-appliances"
  admin@bastion:~$ 

rmusergroup
-----------

`passhport-admin targetgroup delusergroup [(<usergroupname> <targetgroupname>)]` delete the connection between a targetgroup and a usergroup.

================== ===================================================================
Argument           Description
================== ===================================================================
<usergroupname>    Name of the usergroup to disconnect to the targetgroup

<targetname>       Name of the targetgroup of which to disconnect the usergroup
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup rmusergroup linux-admins linux-servers 
  OK: "linux-admins" removed from "linux-servers"
  admin@bastion:~$

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup rmusergroup
  Usergroupname: network-admins 
  Targetgroupname: network-appliances
  OK: "network-admins" removed from "network-appliances"
  admin@bastion:~$ 

addtargetgroup
--------------

`passhport-admin targetgroup addtargetgroup [(<subtargetgroupname> <targetgroupname>)]` connects a subtargetgroup directly to a targetgroup.

==================== ===================================================================
Argument             Description
==================== ===================================================================
<subtargetgroupname> Name of the subtargetgroup to connect to a targetgroup

<targetname>         Name of the targetgroup with which to connect the subtargetgroup
==================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup addtargetgroup linux-servers all-servers 
  OK: "linux-servers" added to "all-servers"
  admin@bastion:~$

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none
 
  admin@bastion:~$ passhport-admin targetgroup addtargetgroup 
  Subtargetgroupname: network-appliances
  Targetgroupname: all-servers
  OK: "network-appliances" added to "all-servers"
  admin@bastion:~$

rmtargetgroup
-------------

`passhport-admin targetgroup deltargetgroup [(<subtargetgroupname> <targetgroupname>)]` delete the connection between a subtargetgroup and a targetgroup.

===================== ===================================================================
Argument              Description
===================== ===================================================================
<subtargetgroupname>  Name of the subtargetgroup to disconnect to a targetgroup

<targetname>          Name of the targetgroup of which to disconnect the subtargetgroup
===================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup rmtargetgroup linux-servers all-servers 
  OK: "linux-servers" removed from "all-servers"
  admin@bastion:~$ 

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup rmtargetgroup
  Subtargetgroupname: network-appliances
  Targetgroupname: all-servers
  OK: "network-appliances" removed from "all-servers"
  admin@bastion:~$ 

delete
-----------

`passhport-admin targetgroup delete [([-f | --force] <name>)]` delete a target.

================== ===================================================================
Argument           Description
================== ===================================================================
<name>             Name of the targetgroup to delete

-f or --force      If used, user won't be prompt for confirmation
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup delete linux-servers 
  Name: linux-servers
  Comment: Linux servers group.
  User list: 
  Target list: linux-7892 linux-7239 linux-1398
  Usergroup list: 
  Targetgroup list: 
  All users: 
  All targets: linux-1398 linux-7239 linux-7892
  All usergroups: 
  All targetgroups: 
  Are you sure you want to delete linux-servers? [y/N] y
  OK: "linux-servers" -> deleted
  admin@bastion:~$ 

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin targetgroup delete
  Name: network-appliances
  Name: network-appliances
  Comment: Network appliance group.
  User list: 
  Target list: 
  Usergroup list: 
  Targetgroup list: 
  All users: 
  All targets: 
  All usergroups: 
  All targetgroups: 
  Are you sure you want to delete network-appliances? [y/N] y
  OK: "linux-servers" -> deleted
  admin@bastion:~$
