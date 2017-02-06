#!/bin/bash -e
VIRTUAL_ENV_PYTHON="$1"

LIST_OF_ARGS=

if [ ! -e "/home/passhport/certs" ]
then
	echo "Certificate directory does not exist, please install certificates (/home/passhport/certs should exist, did you share it correctly ?) !"
	exit 1
fi

if [ ! -r "/home/passhport/certs/cert.pem" ]
then
	echo "Certificate does not exist, please install certificate."
	echo "You can use passhportd docker, that will launch a small wizard on the first run."
	echo "Also, don't forget to share the volume from passhportd docker :"
	echo "- /home/passhport/certs"
	echo "For example, launch passhportd docker like this : "
	echo "$ docker run -t -i -v /var/tmp/dockerpasshportsshdir:/home/passhport/.ssh/ -v /var/tmp/dockerpasshportcerts/ -p 5000:5000 passhportd "
	echo "it will generate certificates, and make them available for the passhport-admin docker."
	echo ""
	echo "Then launch passhport-admin docker with this share volume :"
	echo "$ docker run -t -i -v /var/tmp/dockerpasshportcerts/:/home/passhport/certs"
	exit 1
else
	# We get cert CN to put it into /etc/hosts
	PASSHPORTD_HOSTNAME=`openssl x509 -in /home/passhport/certs/cert.pem -noout -text | grep -e "Subject:.*CN=" | perl -l -p -e 's/.*CN=([^,\s]+)[,\s]*.*$/\1/'`
	IP_GATEWAY=`/sbin/ip route|awk '/default/ { print $3 }'`
	echo "${IP_GATEWAY} ${PASSHPORTD_HOSTNAME}" >> /etc/hosts
	su - passhport -c "sed -i -e 's#^url_passhport =.*#url_passhport = \"https://${PASSHPORTD_HOSTNAME}:5000/\"#' /home/passhport/passhport/passhport_admin/config.py"
fi

shift

# Launch the passhportd in the virtualenv
su - passhport -c "\"${VIRTUAL_ENV_PYTHON}\" /home/passhport/passhport/passhport_admin/passhport-admin $@"
