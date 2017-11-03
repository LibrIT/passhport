#!/bin/bash
PYTHON_ENV=/home/passhport/passhport-run-env
DOCKER_PASSHPORT_SWITCH=$1
shift
ARGS_LIST=$@
case "${DOCKER_PASSHPORT_SWITCH}" in
	passhportd)
		su - passhport -c "/home/passhport/passhport/tools/launch_passhportd_docker.sh ${PYTHON_ENV}"
		;;
	passhport-admin)
		su - passhport -c "/home/passhport/passhport/tools/launch_passhport-admin_docker.sh ${PYTHON_ENV} ${ARGS_LIST}"
		;;
	*)
		echo "Oups ! Launch the correct mode between \"passhportd\" or \"passhport-admin\" when you launch the docker."
		echo "Example : docker run --rm -it -v /var/tmp/passhport-volume:/home/passhport/certs -v /var/tmp/passhport-volume:/var/lib/passhport librit/passhport passhportd"
		exit 1
		;;
esac


