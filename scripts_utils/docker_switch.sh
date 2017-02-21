#!/bin/bash
PYTHON_ENV=$1
shift
DOCKER_PASSHPORT_SWITCH=$2
ARGS_LIST=$@
case "${DOCKER_PASSHPORT_SWITCH}" in
	passhportd)
		/home/passhport/passhport/scripts_utils/launch_passhportd_docker.sh ${PYTHON_ENV}
		;;
	passhport-admin)
		/home/passhport/passhport/scripts_utils/launch_passhport-admin_docker.sh ${PYTHON_ENV} ${ARGS_LIST}
		;;
	*)
		echo "Wrong wrong wrong ! Choose between \"passhportd\" or \"passhport-admin\""
		exit 1
		;;
esac


