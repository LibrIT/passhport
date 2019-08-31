FROM centos:7
MAINTAINER Raphaël Berlamont <raphael.berlamont@librit.fr>
RUN yum install -y epel-release
RUN yum install -y python34-pip git openssl iproute openssh-server
RUN adduser passhport
RUN pip3 install -U pip
RUN pip3 install virtualenv
RUN su - passhport -c "virtualenv -p python3.4 passhport-run-env"
RUN su - passhport -c "/home/passhport/passhport-run-env/bin/pip install pymysql sqlalchemy-migrate flask-migrate requests docopt configparser"
RUN su - passhport -c "git clone http://github.com/LibrIT/passhport.git"
RUN mkdir -p /var/log/passhport/; chown passhport:passhport /var/log/passhport/
RUN mkdir -p /home/passhport/.ssh/; chown passhport:passhport /home/passhport/.ssh/
RUN mkdir -p /var/lib/passhport; chown -R passhport:passhport /var/lib/passhport/
RUN mkdir /etc/passhport && \
	cp /home/passhport/passhport/passhport/passhport.ini /etc/passhport/. && \
	sed -e 's/^LISTENING_IP =.*/LISTENING_IP = 0.0.0.0/' /home/passhport/passhport/passhportd/passhportd.ini > /etc/passhport/passhportd.ini && \
	cp /home/passhport/passhport/passhport-admin/passhport-admin.ini /etc/passhport/.
ENTRYPOINT ["/home/passhport/passhport/tools/docker_switch.sh", "/home/passhport/passhport-run-env/bin/python"]

EXPOSE 5000
EXPOSE 22
