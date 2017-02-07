FROM centos:7
MAINTAINER Raphaël Berlamont <raphael.berlamont@librit.fr>
RUN yum install -y epel-release
RUN yum install -y python34-pip git openssl iproute openssh-server
RUN adduser passhport
RUN pip3 install -U pip
RUN pip3 install virtualenv
RUN su - passhport -c "virtualenv -p python3.4 passhport-run-env"
RUN su - passhport -c "/home/passhport/passhport-run-env/bin/pip install pymysql sqlalchemy-migrate flask-migrate requests docopt"
RUN su - passhport -c "git clone http://github.org/raphux/passhport.git"
RUN mkdir -p /var/log/passhport/; chown passhport:passhport /var/log/passhport/
RUN mkdir -p /home/passhport/.ssh/; chown passhport:passhport /home/passhport/.ssh/
RUN echo 'SSL = "true"' >> "/home/passhport/passhport/passhportd/config.py"
CMD ["/home/passhport/passhport/scripts_utils/launch_passhportd_docker_v0.sh", "/home/passhport/passhport-run-env/bin/python"]

EXPOSE 5000
EXPOSE 22
