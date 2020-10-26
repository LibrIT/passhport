Renew passhportd TLS certificate
===================================

Explanation
-----------

If you installed PaSSHport a year from now, you may encounter this message when you try to connect :

.. code-block:: none

  # ssh passhport@passhport.example.com
  No such user in PaSSHport database.
  tip: it can be a SSL certificate misconfiguration.
  Connection to passhport.example.com closed
  #

This usually means that passhport (the script) can't connect to passhportd, and the most common cause is that the TLS certificate generated on installation is outdated.

.. code-block:: none

  passhport@passhport-srv:~$ openssl x509 -in /home/passhport/certs/cert.pem -noout -text | grep Validity -A 2
        Validity
            Not Before: Sep 11 10:48:55 2020 GMT
            Not After : Sep 11 10:48:55 2021 GMT
  passhport@passhport-srv:~$

As you can see above, the cert is only generated for a year. It has been created on PaSSHport automated installation.


Renew certificate with OpenSSL
------------------------------

To renew the certificate, use the openssl command, as follow :

.. code-block:: none

  root@passhport:~# openssl req -new -key "/home/passhport/certs/key.pem" \
  -config "/home/passhport/passhport/tools/openssl-for-passhportd.cnf" \
  -out "/home/passhport/certs/cert.pem" \
  -subj "/C=FR/ST=Ile De France/L=Ivry sur Seine/O=LibrIT/OU=DSI/CN=passhport.librit.fr" \
  -x509 \
  -days 365 \
  -sha256 \
  -extensions v3_req
  root@passhport:~#

This will generate a self-signed certificate, like the one generated during the installation. It will be valid for 1 year. Change the values to your needs.


Restart passhportd
------------------

You now just need to restart passhportd :

.. code-block:: none

  root@passhport:~# systemctl restart passhportd.service 
  root@passhport:~#

You should now be able to use PaSSHport again.
