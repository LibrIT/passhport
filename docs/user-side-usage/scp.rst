scp through PaSSHport
=============================

Using CLI
------------

**Linux**

To use SCP throug PaSSHport, use one of the following syntax :

From target to local : 

.. code-block:: none

   $ scp -O passhport@my-passhport-server:TARGET_NAME//etc/fstab /tmp/.


From local to target : 

.. code-block:: none

   $ scp -O /etc/passwd passhport@my-passhport-server:TARGET_NAME//tmp/.

NB : the *-O* option is mandatory since ~2021 to force scp to use the legacy *SCP* protocol, instead of *sftp*.


**Windows**

For Windows, you have to consider using "pscp" command. You can find it here: https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html
Be aware that you will need a private key file in "ppk" format. You can use puttygen to generate one or convert your current private key.
Pscp command tries to use SFTP protocol leading to this error: 

.. code-block:: none

   FATAL ERROR: Received unexpected end-of-file from server


In order to use pscp with PaSSHport, consider using this syntax including "-scp" flag:

.. code-block:: none

   pscp -scp -i "C:\path\to\sshkeys\my_private_key.ppk"  "C:\path\to\file\totransfer.txt" passhport@my-passhport-server:TARGET_NAME//pah/to/copy

