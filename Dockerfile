FROM debian:12 as builder

# Update the repos
RUN apt update

# Install package
RUN apt install -y python3-pip python3-venv git openssl libpython3-dev apache2 libapache2-mod-wsgi-py3 libpq-dev bash-completion

# Passhport user creation
RUN /usr/sbin/useradd  --home-dir /home/passhport --shell /bin/bash --create-home --user-group passhport

# Copy sources
RUN mkdir /home/passhport/passhport && chown passhport: /home/passhport/passhport
COPY --chown=passhport:passhport . /home/passhport/passhport

# Create virtual-env
USER passhport
WORKDIR /home/passhport
RUN python3 -m venv passhport-run-env
RUN /home/passhport/passhport-run-env/bin/pip install -r /home/passhport/passhport/requirements.txt
RUN /home/passhport/passhport-run-env/bin/pip install psycopg2 psycopg2-binary flask_login flask_wtf requests

# Make the archive for the final image
RUN tar -cf /tmp/archive.tar -C /home/passhport \
  passhport-run-env \
  passhport/passhportd \
  passhport/passhport \
  passhport/passhport-admin \
  passhport/passhweb \
  passhport/tools/docker \
  passhport/tools/confs \
  passhport/tools/bin

#####################
# FINAL IMAGE build #
#####################
FROM debian:12

# Install minimal python and clean
RUN apt update
RUN apt install -y python3-minimal openssh-client libpq5 bash-completion openssh-server vim
RUN apt clean

# Passhport user creation
RUN /usr/sbin/useradd  --home-dir /home/passhport --shell /bin/bash --create-home --user-group passhport

# Let's get the archive built in the first step
RUN mkdir /home/passhport/passhport && chown passhport: /home/passhport/passhport
COPY --from=builder /tmp/archive.tar /tmp
WORKDIR /home/passhport
RUN tar -xf /tmp/archive.tar 
RUN rm /tmp/archive.tar

# Configure system
RUN mkdir -p "/var/log/passhport" "/var/lib/passhport" "/etc/passhport"
RUN chown -R passhport:passhport "/var/log/passhport" "/var/lib/passhport" "/home/passhport" "/etc/passhport"

RUN mkdir "/etc/bash_completion.d" && cp /home/passhport/passhport/tools/confs/passhport-admin.bash_completion /etc/bash_completion.d/passhport-admin
RUN ln -s /home/passhport/passhport/tools/bin/passhport-admin.sh /usr/local/bin/passhport-admin

# Switch user
USER passhport
WORKDIR /home/passhport

RUN sed \
  -e 's#SQLALCHEMY_DATABASE_DIR\s*=.*#SQLALCHEMY_DATABASE_DIR        = /var/lib/passhport/#'\
  -e 's#LISTENING_IP\s*=.*#LISTENING_IP = 0.0.0.0#'\
  -e 's#SQLALCHEMY_MIGRATE_REPO\s*=.*#SQLALCHEMY_MIGRATE_REPO        = /var/lib/passhport/db_repository#'\
  -e 's#SQLALCHEMY_DATABASE_URI\s*=.*#SQLALCHEMY_DATABASE_URI        = POSTGRESQL_CONNECTION_URI#' \
  "/home/passhport/passhport/passhportd/passhportd.ini" > "/etc/passhport/passhportd.ini"
RUN sed -e "s#PASSHPORTD_HOSTNAME\s*=.*#PASSHPORTD_HOSTNAME = localhost#" "/home/passhport/passhport/passhport-admin/passhport-admin.ini" > "/etc/passhport/passhport-admin.ini"
RUN sed -e "s#PASSHPORTD_HOSTNAME\s*=.*#PASSHPORTD_HOSTNAME = localhost#" "/home/passhport/passhport/passhport/passhport.ini" > "/etc/passhport/passhport.ini"

RUN mkdir /home/passhport/.ssh/ /home/passhport/.sshd
ENTRYPOINT ["/home/passhport/passhport/tools/docker/docker_switch.sh"]

# The volumes
VOLUME /home/passhport/.ssh
VOLUME /home/passhport/.sshd
VOLUME /home/passhport/certs
VOLUME /var/lib/passhport

# Passhportd port
EXPOSE 5000
# PasshWeb port
EXPOSE 5080
# sshd port
EXPOSE 2222
