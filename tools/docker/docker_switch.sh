#!/bin/bash
PYTHON_ENV_RUNTIME=/home/passhport/passhport-run-env/bin/python
echo "ARGUMENTS: ${@}"

DOCKER_PASSHPORT_SWITCH=$2
if [ -z "${DOCKER_PASSHPORT_SWITCH}" ]
then 
  DOCKER_PASSHPORT_SWITCH=passhportd
fi
shift
ARGS_LIST=$@
echo "ARGS_LIST=${ARGS_LIST}; DOCKER_PASSHPORT_SWITCH=${DOCKER_PASSHPORT_SWITCH}"
case "${DOCKER_PASSHPORT_SWITCH}" in
  passhportd)
    bash -xv /home/passhport/passhport/tools/docker/launch_passhportd_docker.sh ${PYTHON_ENV_RUNTIME}
    ;;
  passhport-admin)
    /home/passhport/passhport/tools/docker/launch_passhport-admin_docker.sh ${PYTHON_ENV_RUNTIME} ${ARGS_LIST}
    ;;
  *)
    echo "Oups ! Launch the correct mode between \"passhportd\" or \"passhport-admin\" when you launch the docker."
    echo "Example : docker run --rm -it -v /var/tmp/passhport-volume:/home/passhport/certs -v /var/tmp/passhport-volume:/var/lib/passhport librit/passhport passhportd"
    exit 1
    ;;
esac


