FROM debian:9
MAINTAINER Raphaël Berlamont <raphael.berlamont@librit.fr>
RUN apt update ; apt install -y openssh-server python3-pip git openssl
RUN pip3 install -U pip ; pip3 install virtualenv
RUN useradd --home-dir /home/passhport --shell /bin/bash --create-home passhport
RUN su - passhport -c "virtualenv -p python3 passhport-run-env"
RUN su - passhport -c "/home/passhport/passhport-run-env/bin/pip install pymysql sqlalchemy-migrate flask-migrate requests docopt configparser tabulate"
RUN su - passhport -c "git clone https://github.com/LibrIT/passhport.git"
RUN mkdir -p /var/log/passhport/ ; chown passhport:passhport /var/log/passhport/
RUN mkdir /etc/passhport ; \
	cp /home/passhport/passhport/passhportd/passhportd.ini /etc/passhport/. ; \
	cp /home/passhport/passhport/passhport/passhport.ini /etc/passhport/. ; \
	cp /home/passhport/passhport/passhport_admin/passhport-admin.ini /etc/passhport/. ; \
	cp /home/passhport/passhport/passhportd/passhportd.ini /etc/passhport/.
RUN su - passhport -c '/usr/bin/ssh-keygen -t rsa -b 4096 -N "" -f "/home/passhport/.ssh/id_rsa"'
RUN su - passhport -c '/usr/bin/ssh-keygen -t ecdsa -b 521 -N "" -f "/home/passhport/.ssh/id_ecdsa"'
RUN mkdir -p /var/lib/passhport ; chown -R passhport:passhport /var/lib/passhport/
RUN sed -i -e 's#SQLALCHEMY_DATABASE_DIR\s*=.*#SQLALCHEMY_DATABASE_DIR        = /var/lib/passhport/#' /etc/passhport/passhportd.ini ; \
	sed -i -e 's#LISTENING_IP\s*=.*#LISTENING_IP = 0.0.0.0#' /etc/passhport/passhportd.ini ; \
	sed -i -e 's#SQLALCHEMY_MIGRATE_REPO\s*=.*#SQLALCHEMY_MIGRATE_REPO        = /var/lib/passhport/db_repository#' /etc/passhport/passhportd.ini ; \
	sed -i -e 's#SQLALCHEMY_DATABASE_URI\s*=.*#SQLALCHEMY_DATABASE_URI        = sqlite:////var/lib/passhport/app.db#' /etc/passhport/passhportd.ini ; \
	sed -i -e "s#PASSHPORTD_HOSTNAME\s*=.*#PASSHPORTD_HOSTNAME = `hostname -f`#" /etc/passhport/passhport-admin.ini ; \
	sed -i -e "s#PASSHPORTD_HOSTNAME\s*=.*#PASSHPORTD_HOSTNAME = `hostname -f`#" /etc/passhport/passhport.ini ; 

ENTRYPOINT ["/home/passhport/passhport/scripts_utils/docker_switch.sh", "/home/passhport/passhport-run-env/bin/python"]
