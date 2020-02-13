Connect to PaSSHport
=============================

On Windows
------------

You can use Putty to connect to the passhport bastion indicating your private key.


On Linux / \*nix
--------------------

Use your standard SSH client and connect to the bastion as passhport user:
.. code-block:: none

  ssh passhport@bastion.tld
 
If you want to be directly connected, you have to specify the target name in the command AND to activate the -t option:
.. code-block:: none

  ssh -t passhport@bastion.tld targetname
  
If you want to launch a command directly, you can use the same syntax adding the command at the end
.. code-block:: none

  ssh -t passhport@bastion.tld targetname cat /proc/cpuinfo
