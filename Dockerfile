FROM debian:10
MAINTAINER Raphaël Berlamont <raphael.berlamont@librit.fr>
RUN apt-get update ; apt-get install -y openssh-server python3-pip git openssl curl
RUN tools/passhport-install-script-debian.sh -s
