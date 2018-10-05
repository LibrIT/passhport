Connect to PaSSHport
=============================

On Windows
------------

Well take the 


You can call passhport-admin's CLI, by calling ``passhport-admin`` with the ``-i``.

You can then configure passhportd through this command line. Refer to the good section in the submodule doc to know how to use them.

















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
