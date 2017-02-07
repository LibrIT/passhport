FROM debian:8.7
MAINTAINER Raphaël Berlamont <raphael.berlamont@librit.fr>
RUN apt update
RUN apt install -y python3.4 python3-pip git openssh-server
RUN mkdir /var/run/sshd
RUN sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
RUN useradd --home-dir /home/passhport --shell /bin/bash --create-home passhport
RUN usermod -p`cat /dev/urandom | head -n100 | tr '\n' ' '| sed -e 's/[^a-zA-Z\r\n]//g'` passhport
RUN passwd -u passhport
RUN pip3 install -U pip
RUN pip3 install virtualenv
RUN su - passhport -c "virtualenv -p python3.4 passhport-run-env"
RUN su - passhport -c "/home/passhport/passhport-run-env/bin/pip install pymysql sqlalchemy-migrate flask-migrate requests docopt"
RUN mkdir -p /var/log/passhport/; chown passhport:passhport /var/log/passhport/
RUN mkdir -p /home/passhport/.ssh/; chown passhport:passhport /home/passhport/.ssh/
RUN su - passhport -c "git clone http://github.org/raphux/passhport.git"
CMD ["/home/passhport/passhport/scripts_utils/launch_passhport_docker.sh"]
EXPOSE 22
