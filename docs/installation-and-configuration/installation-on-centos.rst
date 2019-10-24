Installation on CentOS 7
=============================

The followings shows you how to install and run PaSSHport on CentOS 7. We start from a minimal installation of CentOS (available `here <https://www.centos.org/download/>`__).

The easy, automated way
-----------------------
You can review the installation script `here <https://raw.githubusercontent.com/Raphux/passhport/master/tools/passhport-install-script-centos7.sh>`__.

You can run it directly from command line :

.. code-block:: none

  root@centos7:~# bash <(curl -s https://raw.githubusercontent.com/librit/passhport/master/tools/passhport-install-script-centos7.sh)

Once finished, you can go to the `Getting Started <getting-started.html>`_ chapter.


The long, manual way
--------------------

To understand what you do on your system when you install PaSSHport, follow the instructions below, that are more or less the step by step commands from the automated installation script.

Install the EPEL repository : 

.. code-block:: none

  yum install epel-release
  
Install python34-pip and other packages that we’ll need later for this tutorial (it will get ~100MB from the archives, so be patient) :

.. code-block:: none

  root@centos7:~# yum install python34-pip git openssl python34-devel gcc

Let’s update pip :

.. code-block:: none

  root@centos7:~# pip3 install -U pip

Now, install virtual-env using pip :

.. code-block:: none

  root@centos7:~# pip3 install virtualenv

Next we will need to add a system user called « passhport », and switch to it :

.. code-block:: none

  root@centos7:~# useradd --home-dir /home/passhport --shell /bin/bash --create-home passhport
  root@centos7:~# su - passhport
  passhport@centos7:~$

We now need to create a virtual-env for passhport user :

.. code-block:: none

  passhport@centos7:~$ virtualenv -p python3 passhport-run-env

Now that we have our virtual-env, we install the python’s modules we’ll need for PaSSHport :

.. code-block:: none

  passhport@centos7:~$ /home/passhport/passhport-run-env/bin/pip install sqlalchemy-migrate flask-migrate requests docopt configparser tabulate flask-login ldap3 psutil cryptography

Now, let’s start the real thing…

Let’s get passhport sources from github :

.. code-block:: none

  passhport@centos7:~$ git clone http://github.com/LibrIT/passhport.git
  Clonage dans 'passhport'...
  remote: Counting objects: 2713, done.
  remote: Compressing objects: 100% (50/50), done.
  remote: Total 2713 (delta 19), reused 0 (delta 0), pack-reused 2661
  Réception d'objets: 100% (2713/2713), 482.76 KiB | 396.00 KiB/s, fait.
  Résolution des deltas: 100% (1633/1633), fait.
  passhport@centos7:~$

PaSSHport will need to write some logs, so, as root, we’ll create a directory in « /var/log », and give the ownership to the « passhport » user:

.. code-block:: none

  root@centos7:~# mkdir -p /var/log/passhport/
  root@centos7:~# chown passhport:passhport /var/log/passhport/

We’ll also create the config directory, and copy the differents config file :

.. code-block:: none

  root@centos7:~# mkdir /etc/passhport
  root@centos7:~# cp /home/passhport/passhport/passhport/passhport.ini /etc/passhport/.
  root@centos7:~# cp /home/passhport/passhport/passhport-admin/passhport-admin.ini /etc/passhport/.
  root@centos7:~# cp /home/passhport/passhport/passhportd/passhportd.ini /etc/passhport/.

We’ll also need to make some modifications in those config file, if you run passhportd on a distant server. Here we’ll change the default listening address (localhost) to the real IP of our server.

First, passhportd :

.. code-block:: none

  root@centos7:~# vim /etc/passhport/passhportd.ini

Change the « LISTENING_IP » parameter, to the IP address of your server :

.. code-block:: none

  # Passhportd configuration file. You should copy it to
  # /etc/passhport/passhportd.ini if you want to do modifications
  [SSL]
  SSL = True
  SSL_CERTIFICAT = /home/passhport/certs/cert.pem
  SSL_KEY = /home/passhport/certs/key.pem
  
  [Network]
  LISTENING_IP = 192.168.122.56
  PORT = 5000
  
  [Database]
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  SQLALCHEMY_DATABASE_DIR = /var/lib/passhport/
  SQLALCHEMY_MIGRATE_REPO = /var/lib/passhport/db_repository
  # For SQLite
  SQLALCHEMY_DATABASE_URI = sqlite:////var/lib/passhport/app.db
  
  [Environment]
  # SSH Keyfile path
  SSH_KEY_FILE = /home/passhport/.ssh/authorized_keys
  # Python and passhport paths
  PASSHPORT_PATH = /home/passhport/passhport/passhport/passhport
  PYTHON_PATH = /home/passhport/passhport-run-env/bin/python3

Change the following parameter in /etc/passhport/passhport.ini and /etc/passhport/passhport-admin.ini :

``PASSHPORTD_HOSTNAME = 192.168.122.56``

We’ll need ssh publickey, so we generate an 4096 bits RSA key:

.. code-block:: none

  root@centos7:~# su - passhport
  passhport@centos7:~$ ssh-keygen -t rsa -b 4096 -N "" -f "/home/passhport/.ssh/id_rsa"
  Generating public/private rsa key pair.
  Your identification has been saved in /home/passhport/.ssh/id_rsa.
  Your public key has been saved in /home/passhport/.ssh/id_rsa.pub.
  The key fingerprint is:
  SHA256:0o6jkepqr2Phz0AKmLGRZh6PeVexP2gf5CGNPd+ksQ passhport@centos7
  The key's randomart image is:
  +---[RSA 4096]----+
  | .    ....       |
  |oo . o .+ +      |
  |* + o ...= *     |
  |.O   o oo + E    |
  |=.    LibrIT .   |
  |+.   .Rocks = .  |
  |o.. o o .  . o   |
  | =o. o .         |
  |++B+.            |
  +----[SHA256]-----+
  passhport@centos7:~$

This will be the key that’ll be use by PaSSHport to connect to your hosts. You can also generate a ECDSA key if you wish :

.. code-block:: none

  passhport@centos7:~$ ssh-keygen -t ecdsa -b 521 -N "" -f "/home/passhport/.ssh/id_ecdsa"

Again as root, let’s make the directory that’ll contains the database (because we use SQLite for this tutorial) :

.. code-block:: none

  root@centos7:~# mkdir -p /var/lib/passhport
  root@centos7:~# chown -R passhport:passhport /var/lib/passhport/

… then we’ll have to change 3 paramaters in the passhportd config file (as root, edit «/etc/passhport/passhportd.ini») :

.. code-block:: none

  SQLALCHEMY_DATABASE_DIR        = /var/lib/passhport/
  SQLALCHEMY_MIGRATE_REPO        = /var/lib/passhport/db_repository
  SQLALCHEMY_DATABASE_URI        = sqlite:////var/lib/passhport/app.db

Now we can create the database and check that it has correcly been created:

.. code-block:: none

  root@centos7:~# su - passhport
  passhport@centos7:~$ /home/passhport/passhport-run-env/bin/python /home/passhport/passhport/passhportd/db_create.py
  passhport@centos7:~$ ls -la /var/lib/passhport/
  total 172
  drwxr-xr-x  3 passhport passhport   4096 févr. 28 16:10 .
  drwxr-xr-x 25 root      root        4096 févr. 28 15:37 ..
  -rw-r--r--  1 passhport passhport 159744 févr. 28 16:10 app.db
  drwxr-xr-x  4 passhport passhport   4096 févr. 28 16:10 db_repository
  passhport@centos7:~$

We’ll now need to create the certificate to secure the API. First, create the directory in which will be key and the cert, and make the directory rwx for passport only :

.. code-block:: none

  passhport@centos7:~$ mkdir /home/passhport/certs
  passhport@centos7:~$ chmod 700 /home/passhport/certs

Create the RSA key :

.. code-block:: none

  [passhport@centos-7 ~]$ openssl genrsa -out "/home/passhport/certs/key.pem" 4096

There is a conf file provided for OpenSSL, to generate a minimal correct SSL cert. The file is :

``/home/passhport/passhport/tools/openssl-for-passhportd.cnf``

Edit it, and add DNS name you’ll use to reach the API. For the tutorial, we’ll use two hostnames (localhost added) :

.. code-block:: none

  [req]
  distinguished_name      = req_distinguished_name
  req_extensions          = v3_req
  subjectKeyIdentifier    = hash
  authorityKeyIdentifier  = keyid:always,issuer
  
  [v3_req]
  subjectAltName          = @alternate_names
  basicConstraints        = CA:TRUE
  subjectKeyIdentifier    = hash
  authorityKeyIdentifier  = keyid:always,issuer
  
  [req_distinguished_name]
  
  [ alternate_names ]
  DNS.1 = localhost
  DNS.2 = passhport.librit.fr
  DNS.3 = entry.passhport.org

Now, generate the certificate using this command (put on multiple lines, so you can copy/paste easily), but please adapt the subject line (-subj) :

.. code-block:: none

  openssl req -new -key "/home/passhport/certs/key.pem" \
  -config "/home/passhport/passhport/tools/openssl-for-passhportd.cnf" \
  -out "/home/passhport/certs/cert.pem" \
  -subj "/C=FR/ST=Ile De France/L=Ivry sur Seine/O=LibrIT/OU=DSI/CN=passhport.librit.fr" \
  -x509 -days 365 -sha256 \
  -extensions v3_req

Once executed, you’ll have a cert file next to the key file :

.. code-block:: none

  passhport@centos7:~$ ls -la /home/passhport/certs/
  total 16
  drwx------ 2 passhport passhport 4096 févr. 28 18:00 .
  drwxr-xr-x 8 passhport passhport 4096 févr. 28 17:46 ..
  -rw-r--r-- 1 passhport passhport 2171 févr. 28 18:00 cert.pem
  -rw------- 1 passhport passhport 3243 févr. 28 16:11 key.pem
  passhport@centos7:~$

As root, create some symlink to the two main *binaries*, passhportd and passhport-admin, so you can access it without typing full path :

.. code-block:: none

  root@centos7:~# ln -s /home/passhport/passhport/tools/passhportd.sh /usr/bin/passhportd
  root@centos7:~# ln -s /home/passhport/passhport/tools/passhport-admin.sh /usr/bin/passhport-admin

We now create the systemd service, and enables *passhportd* on startup :

.. code-block:: none

  root@centos7:~# cp /home/passhport/passhport/tools/passhportd.service /etc/systemd/system/passhportd.service
  root@centos7:~# systemctl daemon-reload
  root@centos7:~# systemctl enable passhportd

And now, we’re ready to go, just launch passhportd daemon :

.. code-block:: none

  root@centos7:~# systemctl start passhportd

You can check that passhportd is running, by curling the IP you previously configured in */etc/passhport/passhportd.ini*, on port 5000 :

.. code-block:: none

  root@centos7:~# curl -s --insecure https://192.168.122.56:5000
  passhportd is running, gratz!
  root@centos7:~#

Bravo ! You successfully installed PaSSHport. You may now go to the `Getting Started <getting-started.html>`_ chapter.
