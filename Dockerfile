FROM debian:13
# Update the repos
RUN apt update

# Get the corresponding installation file
COPY . /tmp/passhport

# Proceed with installation
RUN bash -xv /tmp/passhport/tools/install/install_debian_13.sh -sd
RUN rm -rf /tmp/passhport
