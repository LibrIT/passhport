FROM httpd:2.4.41
MAINTAINER Raphaël Berlamont <raphael.berlamont@librit.fr>
RUN apt-get update ; apt-get install -y openssh-server python3-pip git openssl curl
ADD . /tmp/passhport-dockerbuild/
WORKDIR "/tmp/passhport-dockerbuild/"
ENV PASSHPORT_SOURCES_DIR "/tmp/passhport-dockerbuild/"
RUN bash tools/passhport-install-script-debian.sh -s -c
RUN mkdir /run/sshd
ENTRYPOINT ["/home/passhport/passhport/tools/docker_switch.sh"]
