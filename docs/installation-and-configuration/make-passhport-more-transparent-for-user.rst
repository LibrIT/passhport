Make passhport more transparent for user
========================================

It is possible to configure passhport in a way that it is pretty transparent for users.

First you need to allow passing a the environment variable PASSHPORT_TARGET to sshd:

.. code-block:: none

  echo "AcceptEnv PASSHPORT_TARGET" >> /etc/ssh/sshd_config
  systemctl restart ssh


Then you can setup a ssh client like this :

.. code-block:: none

  Host myhost
    User passhport
    Hostname mybastion
    SetEnv PASSHPORT_TARGET=myhost
    SendEnv PASSHPORT_TARGET

And then use ssh normally

  ssh myhost

or in a command line (e.g for automation tools)

.. code-block:: none

  PASSHPORT_TARGET=myhost ssh -o "SendEnv PASSHPORT_TARGET" passhport@mybastion

