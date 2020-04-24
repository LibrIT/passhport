Generate private keys
=============================

Change password on every connection :
--------------------------------------

For security purpose, you can configure PaSSHport to change the password of the user@target you just connected to. This can NOT be set per target, if you set this, the password we'll be change for *all* targets. 

To do this, edit the *passhportd.ini* file (``/etc/passhport/passhportd.ini``), and set the parameter : :


To generate the public key (extract from the along side generated private key) that you'll give to your PaSSHport admin, use `puttygen` that you can download from `here <https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>`__ (search for `puttygen.exe`).


Start puttygen, and on the main windows, select the type of key you want to generate (`1`), the key length (`2`), then click `Generate` button (`3`). Here, we selected RSA and a key length of 4096 (2048 is a considered as a minimum for RSA) :

.. image:: images/doc-passhport-puttygen-0.png

Move your mouse in the blank space, until the key is generated :

.. image:: images/doc-passhport-puttygen-1.png

Once generated, insert a comment (`1`), a strong passphrase (`2`), then save your private key (`3`).

.. image:: images/doc-passhport-puttygen-2.png

You now have to send your RSA public key to your PaSSHport admin. Select your public key as shown in this screen capture, and copy/paste it into a mail to your PaSSHport admin :

.. image:: images/doc-passhport-puttygen-3.png

You now have to wait until your PaSSHport admin add your key to your account into PaSSHport.

On Linux / Unix :
-------------------

Simply open a terminal, and use the `ssh-keygen` command. Here we generate à 4096bits length RSA key :

.. code-block:: none

  user@host:~$ ssh-keygen -t rsa -b 4096
  Generating public/private rsa key pair.
  Enter file in which to save the key (/home/user/.ssh/id_rsa): 
  Created directory '/home/user/.ssh'.
  Enter passphrase (empty for no passphrase): 
  Enter same passphrase again: 
  Your identification has been saved in /home/user/.ssh/id_rsa.
  Your public key has been saved in /home/user/.ssh/id_rsa.pub.
  The key fingerprint is:
  SHA256:1r28XcYMIclivAHSSqmzH5Dh1LJ+IMsQMhl2Ds1HtXQ user@passhport-debian9-dev
  The key's randomart image is:
  +---[RSA 4096]----+
  |.=o..oo=.E       |
  |* +o+.=.+o . .   |
  |.o +.B o  = + .  |
  |. . O .  o = . . |
  | o + =  S o . .  |
  |  o o o.   . . + |
  |     o .    o   =|
  |      .      o o |
  |            . .  |
  +----[SHA256]-----+
  user@host:~$

Display your newly created public key :

.. code-block:: none

  user@host:~$ cat .ssh/id_rsa.pub 
  ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDmcmVG6uGW3BvOkHN7M7ubITihVwL9glc7jilZvzgDJL4CzCXG2VwjdxHaCBfW82HsgoUcwqKm1gMfYv/TEZw/tgUWSSo7TOmldFmEs4TmZc9n0lhCgGT/XtShqtwyYAxeAw419Uc+L/unXKPRtulLjNqdp62GW68CTQ7GzJosDWLYWZfNrhRoMvw6K6j/vLbVcoktY+RNoNdFjYhgPcKzP0p73pvlh9uIKohBkh3vh5pOfVEu6L9J4VvjM3dACScPJORG05N7MB4rJ3FpSy9fgfMwaT99Xm7/IVKXZxoUjB9z2EBkKYK+Hlj5Oopwgas6AvcrJIdZo1tsbdUYqcbQKoX7TeSwjbxESygFuCLMgs4SuMy8/1+pPIlJQY7XzdCCDzkEp/s12Ca5xPSUpFGdWKKIf1jzZzjS5BeUzm63ldFoN+HHKuU7FRpPNSXrlWNkqkwHnpa1SbhT3yOlu6BdnxMcaRNAeQ+cfxyykUSdoPQWBiJ9QSd796PgMSJG135ZrZrBj86l7FbKHnnSbfcwoRaaejsaD9Pj0KuZ9l9Aiy69pobkAvzm4oCeORjIVeQo1k8mFPVPli9C5yM7iQzYahJDP9SGG4sZPsONFVsm2cugVqT3jaYBBQH5PWsZJN46mz6vqzkPTYO/toXNiXpyhrg3RT35Pj96cx7nwg9CrQ== user@passhport-debian9-dev
  user@host:~$ 

And send this content to your PaSSHport admin. You now have to wait until your PaSSHport admin add your key to your account into PaSSHport.

