FROM centos:7
MAINTAINER Raphaël Berlamont <raphael.berlamont@librit.fr>
RUN yum install -y epel-release
RUN yum install -y  python34-pip git openssl iproute
RUN adduser passhport
RUN pip3 install -U pip
RUN pip3 install virtualenv
RUN su - passhport -c "virtualenv -p python3.4 passhport-run-env"
RUN su - passhport -c "/home/passhport/passhport-run-env/bin/pip install pymysql sqlalchemy-migrate flask-migrate requests docopt"
RUN su - passhport -c "git clone http://github.org/raphux/passhport.git"

ENTRYPOINT ["/home/passhport/passhport/scripts_utils/launch_passhport-admin_docker.sh", "/home/passhport/passhport-run-env/bin/python"]

CMD [""]
