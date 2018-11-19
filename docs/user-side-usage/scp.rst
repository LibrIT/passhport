scp through PaSSHport
=============================

Using CLI
------------

To use SCP throug PaSSHport, use one of the following syntax...

From target to local : 

.. code-block:: none

   $ scp passhport@my-passhport-server:TARGET_NAME//etc/fstab /tmp/.


From local to target : 

.. code-block:: none

   $ scp /etc/passwd passhport@my-passhport-server:TARGET_NAME//tmp/.

