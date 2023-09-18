FROM debian:12
# Update the repos
RUN apt update

# Get the corresponding installation file
COPY tools/install/install_debian_12.sh /tmp/install_debian_12.sh

# start
RUN bash -xv /tmp/install_debian_12.sh -sd
