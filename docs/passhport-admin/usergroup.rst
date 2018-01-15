usergroup
=============================

Usages :

.. code-block:: none

  passhport-admin usergroup list
  passhport-admin usergroup search [<pattern>]
  passhport-admin usergroup show [<name>]
  passhport-admin usergroup create [(<name> [--comment=<comment>])]
  passhport-admin usergroup edit [(<name> [--newname=<name>] [--newcomment=<comment>])]
  passhport-admin usergroup (adduser | rmuser) [(<username> <usergroupname>)]
  passhport-admin usergroup (addusergroup | rmusergroup) [(<subusergroupname> <usergroupname>)]
  passhport-admin usergroup delete [([-f | --force] <name>)]


list
-----

`passhport-admin usergroup list` show all the configured usergroups.

**Example :**

.. code-block:: none
  
  admin@bastion:~$ passhport-admin usergroup list
  admins
  database-admins
  external
  network-admins
  admin@bastion:~$

search
---------

`passhport-admin usergroup search [<PATTERN>]` searches in the usergroup list for all usergroups that correspond to the given pattern.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup search ext
  external
  admin@bastion:~$

If no pattern is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup search 
  Pattern: admins
  admins
  database-admins
  network-admins
  admin@bastion:~$

show
-------

`passhport-admin usergroup show <NAME>` shows informations about the usergroup <NAME>.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup show admins 
  Name: admins
  Comment: 
  User list: john@compagny.com vincent@compagny.com
  Usergroup list: 
  All users: john@compagny.com vincent@compagny.com
  All usergroups: 
  admin@bastion:~$

If no pattern is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup show
  Name: admins
  Name: admins
  Comment: 
  User list: john@compagny.com vincent@compagny.com
  Usergroup list: 
  All users: john@compagny.com vincent@compagny.com
  All usergroups: 
  admin@bastion:~$

create
----------

`passhport-admin usergroup create [(<name> [--comment=<comment>])]` creates a new usergroup.

================== ===================================================================
Argument           Description
================== ===================================================================
<name>             Name of the usergroup to create

--comment          Comment concerning the usergroup (optional)
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup create external
  OK: "external" -> created
  admin@bastion:~$

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup delete database-admins
  Name: database-admins
  Comment: 
  User list: 
  Usergroup list: 
  All users: 
  All usergroups: 
  Are you sure you want to delete database-admins? [y/N] y
  OK: "database-admins" -> deleted
  admin@bastion:~$

edit
-----------

`passhport-admin usergroup edit [(<name> [--newname=<name>] [--newcomment=<comment>])]` edits an existing usergroup.

================== ===================================================================
Argument           Description
================== ===================================================================
<name>             Name of the usergroup to edit

--newname          New name of the usergroup if you want to rename it (optional)

--newcomment       New comment concerning the usergroup (optional)
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup edit admins --newname=linux-admins
  OK: "admins" -> edited
  admin@bastion:~$ 

If no argument is given, user enters in interactive mode. It firsts shows all parameters of the usergroup, then displays each parameters for a change. User can keep any previous configured parameter, just by typing "Enter". They only exception is the comment. If user wants to remove the comment, he just type "Enter", and will then be asked if the original comment should be removed or not.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup edit 
  Name of the usergroup you want to modify: external
  Name: external
  Comment: 
  User list: 
  Usergroup list: 
  All users: 
  All usergroups: 
  New name: external-admins
  New comment: 
  Remove original comment? [y/N] 
  OK: "external" -> edited
  admin@bastion:~$ 

As you can see above, we only changed the "New name" entry. If an entry is simply replied with "enter", it keeps the previous value.

adduser
-----------

`passhport-admin usergroup adduser [(<username> <usergroupname>)]` add a user in a usergroup.

================== ===================================================================
Argument           Description
================== ===================================================================
<username>         Name of the user to add in a usergroup

<usergroupname>    Name of the usergroup in which to add the user
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup adduser vincent@compagny.com network-admins 
  OK: "vincent@compagny.com" added to "network-admins"
  admin@bastion:~$

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup adduser 
  Username: yann@ext-compagny.com
  Usergroupname: external-admins
  OK: "yann@ext-compagny.com" added to "external-admins"
  admin@bastion:~$

rmuser
-----------

`passhport-admin usergroup rmuser [(<username> <usergroupname>)]` removes a user from a usergroup.

================== ===================================================================
Argument           Description
================== ===================================================================
<username>         Name of the user to remove from a usergroup

<usergroupname>    Name of the usergroup of which to remove the user
================== ===================================================================

**Example :**

.. code-block:: none
  
  admin@bastion:~$ passhport-admin usergroup rmuser vincent@compagny.com linux-admins 
  OK: "vincent@compagny.com" removed from "linux-admins"
  admin@bastion:~$

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup rmuser 
  Username: yann@ext-compagny.com
  Usergroupname: external-admins
  OK: "yann@ext-compagny.com" removed from "external-admins"
  admin@bastion:~$ 

addusergroup
-------------

`passhport-admin usergroup addusergroup [(<subusergroupname> <usergroupname>)]` adds a usergroup in another usergroup.

================== ===================================================================
Argument           Description
================== ===================================================================
<subusergroupname>    Name of the usergroup to add in a usergroup

<usergroupname>    Name of the usergroup in which to add the usergroup
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup addusergroup linux-admins admins 
  OK: "linux-admins" added to "admins"
  admin@bastion:~$

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup addusergroup
  Subusergroupname: network-admins
  Usergroupname: admins
  OK: "network-admins" added to "admins"
  admin@bastion:~$

rmusergroup
-----------

`passhport-admin usergroup rmusergroup [(<subusergroupname> <usergroupname>)]` delete the connection between a usergroup and a usergroup.

================== ===================================================================
Argument           Description
================== ===================================================================
<subusergroupname> Name of the usergroup to remove from a usergroup

<usergroupname>    Name of the usergroup of which to remove the usergroup
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup rmusergroup linux-admins admins 
  OK: "linux-admins" removed from "admins"
  admin@bastion:~$

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup rmusergroup 
  Subsergroupname: network-admins
  Usergroupname: admins
  OK: "network-admins" removed from "admins"
  admin@bastion:~$ 

delete
-----------

`passhport-admin usergroup delete [([-f | --force] <name>)]` delete a usergroup.

================== ===================================================================
Argument           Description
================== ===================================================================
<name>             Name of the usergroup to delete

-f or --force      If used, user won't be prompt for confirmation
================== ===================================================================

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup delete network-admins 
  Name: network-admins
  Comment: 
  User list: vincent@compagny.com
  Usergroup list: 
  All users: vincent@compagny.com
  All usergroups: 
  Are you sure you want to delete network-admins? [y/N] y
  OK: "network-admins" -> deleted
  admin@bastion:~$

If no argument is given, user enters in interactive mode.

**Example :**

.. code-block:: none

  admin@bastion:~$ passhport-admin usergroup delete
  Name: linux-admins
  Name: linux-admins
  Comment: 
  User list: john@compagny.com
  Usergroup list: 
  All users: john@compagny.com
  All usergroups: 
  Are you sure you want to delete linux-admins? [y/N] y
  OK: "network-admins" -> deleted
  admin@bastion:~$
