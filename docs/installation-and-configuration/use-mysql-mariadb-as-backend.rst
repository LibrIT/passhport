Use MySQL as database backend
===================================

Install PyMySQL python module
-----------------------------------------------

If you did not use the packaged version of passhport (deb/rpm), proceed as follow. If you used the package version, go directly below, to the `MySQL configuration`_.

If you want to use MySQL as the database backend you'll need to add a python module : PyMySQL.

As passhport user, install PyMySQL : 

.. code-block:: none

  $ /home/passhport/passhport-run-env/bin/pip install PyMySQL

MySQL configuration
-------------------------

Create a *passhport* database in you MySQL server (may be different on your distro, this is just an example) :

.. code-block:: none

  # mysql -u root
  Welcome to the MariaDB monitor.  Commands end with ; or \g.
  Your MariaDB connection id is 2
  Server version: 5.5.56-MariaDB MariaDB Server

  Copyright (c) 2000, 2017, Oracle, MariaDB Corporation Ab and others.

  Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

  MariaDB [(none)]> CREATE DATABASE passhport;
  Query OK, 1 row affected (0.00 sec)

Then create a user that'll have all rights on the *passhport* database :

.. code-block:: none

  MariaDB [(none)]> GRANT ALL PRIVILEGES ON passhport.* TO passhport@localhost IDENTIFIED BY 'iwetoh3oochieshaRei4';
  Query OK, 0 rows affected (0.00 sec)

  MariaDB [(none)]> Bye

  #


passhportd configuration
-------------------------

Change the configuration of the *passhportd.ini* file (``/etc/passhport/passhportd.ini``). You need to change the ``SQLALCHEMY_DATABASE_URI`` parameter to :

.. code-block:: none

  SQLALCHEMY_DATABASE_URI        = mysql+pymysql://passhport:iwetoh3oochieshaRei4@localhost/passhport

As passhport (system) user, initialize the database : 

.. code-block:: none

  $ /home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/db_create.py

Re-launch passhportd (as root) :

.. code-block:: none

  # systemctl restart passhportd

PaSSHport now use MySQL backend.
