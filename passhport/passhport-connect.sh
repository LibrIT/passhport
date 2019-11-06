#/usr/bin/env bash 
# Part of the passhport connection script

###### INITIALIZATION ########
FILELOG=$1
PORT=$2
LOGIN=$3
TARGET=$4
PID=$5
URL=$6
CERT=$7
OPTION="$@"
USERNAME="$8"
OPTIONS=""
KEEPCONNECT="$(grep '^KEEPCONNECT[[:space:]]=[[:space:]]True$' /etc/passhport/passhport.ini | wc -l)"
PASSHHOMEDIR="/home/passhport"
PYTHONBIN="${PASSHHOMEDIR}/passhport-run-env/bin/python3"
PASSHPORTBIN="${PASSHHOMEDIR}/passhport/passhport/passhport"



###### We trap a manual window close to let the script to end ######
trap "echo 'You are not allowed to stop disconnection. Consider Ctrl-D.'" SIGHUP SIGINT SIGKILL SIGTERM SIGSTOP

#Remove 7 first arguments and put the others in the OPTIONS variable
i=0
for option in ${OPTION}
do
    if [ "$i" -lt "8" ]
    then
        i=$(($i +1))
    else
        OPTIONS="${OPTIONS} ${option}"
    fi
done

###### SSH CONNECTION ########
script -q --timing=${FILELOG}.timing ${FILELOG} -c "ssh -t -p ${PORT} ${LOGIN}@${TARGET} ${OPTIONS}"
###### CALL PASSHPORTD TO END SESSION ######
if [ "${CERT}" == "/dev/null" ]
then
    wget -qO - ${URL}connection/ssh/endsession/${PID} &> /dev/null
else
    wget --ca-certificate=${CERT} -qO - ${URL}connection/ssh/endsession/${PID} &> /dev/null
fi

# Launch PaSSHport with the same user after the connection
# If it's a direct connection, we don't connect again
if [ "${KEEPCONNECT}" -eq "1" ] && [ -z "${SSH_ORIGINAL_COMMAND}" ]
then
    exec ${PYTHONBIN} ${PASSHPORTBIN} ${USERNAME} 
fi
