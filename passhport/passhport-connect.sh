#/usr/bin/env bash -x
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
OPTIONS=""

###### We trap a manual window close to let the script to end ######
trap "echo Ending script" SIGHUP SIGINT SIGKILL SIGTERM SIGSTOP

#Remove 7 first arguments and put the others in the OPTIONS variable
i=0
for option in ${OPTION}
do
    if [ "$i" -lt "7" ]
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
