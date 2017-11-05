Use PostgreSQL as database backend
===================================

Install psycopg2 python module
-----------------------------------------------

If you did not use the packaged version of passhport (deb/rpm), proceed as follow. If you used the package version, go directly below, to the `PostgreSQL configuration`_.

If you want to use PostgreSQL has the database backend you'll need to add a python module : psycopg2.

As passhport user, install psycopg2 : 

.. code-block:: none

  $ /home/passhport/passhport-run-env/bin/pip install psycopg2

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

passhportd configuration
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
