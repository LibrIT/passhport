Use PostgreSQL as database backend
===================================

Install psycopg2 and psycopg2-binary python modules
---------------------------------------------------

If you did not use the packaged version of passhport (deb/rpm), proceed as follow. If you used the package version, go directly below, to the `PostgreSQL configuration`_.

Before installing python libs, be sure to have *pg_config* in your $PATH and some postgres libraries.

For Debian, install *postgresql-common* and *postgresql-server*

.. code-block:: none

  # apt install postgresql-common postgresql-server

For CentOS, install `postgresql` :

.. code-block:: none

  # yum install postgresql

If you want to use PostgreSQL as the database backend you'll need to add two python modules : psycopg2 and psycopg2-binary.

As passhport user, install psycopg2 and psycopg2-binary: 

.. code-block:: none

  $ /home/passhport/passhport-run-env/bin/pip install psycopg2 psycopg2-binary

PostgreSQL configuration
-------------------------

Create a passhport user in you postgreSQL server (may be different on your distro, this is just an example) :

.. code-block:: none

  # su - postgres
  $ createuser -D -S -R passhport && createdb -O passhport "passhport"

Add a password to postgreSQL passhport user :

.. code-block:: none

  $ psql
  psql (9.2.18)
  Type "help" for help.

  postgres=# ALTER USER "passhport" WITH PASSWORD 'MySUpErp45sw0rD';
  ALTER ROLE
  postgres=# \q
  $

Passhportd configuration
-------------------------

Change the configuration of the *passhportd.ini* file (``/etc/passhport/passhportd.ini``). You need to change the ``SQLALCHEMY_DATABASE_URI`` parameter to :

.. code-block:: none

  SQLALCHEMY_DATABASE_URI        = postgresql://passhport:MySUpErp45sw0rD@localhost/passhport

As passhport (system) user, initialize the database : 

.. code-block:: none

  $ /home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/db_create.py

Then you can launch *passhportd* (kill it before if it stills running) :

.. code-block:: none

  $ /home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/passhportd

PaSSHport now use PostgreSQL backend.
