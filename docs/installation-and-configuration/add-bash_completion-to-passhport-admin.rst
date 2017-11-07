Add bash_completion capability to passhport-admin
==================================================

We provide a bash_completion file, so that you can use [TAB] to auto-complete the passhport-admin command.

As root, copy the provide file to `/etc/bash_completion/passhport-admin` directory, and source it :

.. code-block:: none

  # cp /home/passhport/passhport/tools/passhport-admin.bash_completion /etc/bash_completion.d/passhport-admin
  # . /etc/bash_completion.d/passhport-admin

You can now do things like these :

.. code-block:: none

  # passhport-admin [TAB][TAB]
  target user targetgroup usergroup
  # passhport-admin t[TAB]
  # passhport-admin target[TAB]
  target targetgroup
  # passhport-admin targetg[TAB]
  # passhport-admin targetgroup [TAB][TAB]
  list search show create edit adduser rmuser
  addtarget rmtarget addusergroup rmusergroup 
  addtargetgroup rmtargetgroup delete


  # passhport-admin user show [TAB][TAB]
  john rachel alfred bruce kim jared
  # passhport-admin user show j[TAB]
  john jared
  # passhport-admin user show ja[TAB]
  # passhport-admin user show jared

The end.
