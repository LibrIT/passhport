Getting started
###############

So you now have a brand new installation of PaSSHport, but you don't know what to do next…

Example prerequisites
=====================
For this tutorial, we will use the following infos :

1 PaSSHport node
----------------
We'll use a monolithic installation of PaSSHport : passhportd, passhport and passhport-admin are on the same host.

3 users
--------
* John, a linux/unix administrator, who needs to access all linux/unix servers
* Vincent, a network administrator, who needs to access all network appliances
* Alice, a general appliance administrator who needs to access all tier appliances
* Yann, a consultant who's here for a temporary mission about storage infrastructure, that need to access the NAS server and a the SAN bay

1 PaSSHport admin
------------------
* Marc, the ISSM, who configures PaSSHport, to control all the access rights

3 types of targets
-------------------
* Linux/Unix servers :
 - 1 web server, Linux, www-server / 10.0.1.24
 - 1 VPN server, OpenBSD, vpn-srv1 / 10.0.23.51
 - 1 NAS server, FreeBSD, nas-srv1 / 10.0.12.87
* Network appliances
 - 1 WiFi access points, net-AP9-23 / 172.22.9.23
 - 1 router, net-RO10-98 / 172.16.10.98
 - 1 network switch, net-SW22-57 / 172.20.22.57
* Other appliances
 - 1 IPBX, ipbx1 / 10.192.98.76
 - 1 Network printer, prntr44 / 192.168.254.44
 - 1 SAN bay, san1 / 10.192.1.10

Configure targets
-----------------
First of all, we'll include the targets into PaSSHport.

Let's connect to your PaSSHport node, and add the linux target :

