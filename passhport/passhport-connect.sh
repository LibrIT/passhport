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
TARGETNAME="$9"
EXPIRES_AT="${10}"
export EXPIRES_AT
OPTIONS="-C -o ControlMaster=auto -o ControlPersist=60s -o ControlPath=/tmp/socket-%u-to-%r@%h:%p"
KEEPCONNECT="$(grep '^KEEPCONNECT[[:space:]]=[[:space:]]True$' /etc/passhport/passhport.ini | wc -l)"
PASSHHOMEDIR="/home/passhport"
PYTHONBIN="${PASSHHOMEDIR}/passhport-run-env/bin/python3"
PASSHPORTBIN="${PASSHHOMEDIR}/passhport/passhport/passhport"



###### We trap a manual window close to let the script to end ######
trap "echo 'You are not allowed to stop disconnection. Consider Ctrl-D.'" SIGHUP SIGINT SIGKILL SIGTERM SIGSTOP

#Remove 10 first arguments and put the others in the OPTIONS variable
i=0
for option in ${OPTION}
do
    if [ "$i" -lt "10" ]
    then
        i=$(($i +1))
    else
        OPTIONS="${OPTIONS} ${option}"
    fi
done

EXPIRED_NOTICE="/tmp/passhport-expired-${USERNAME}"
if [ -n "${EXPIRES_AT}" ] && [ "${EXPIRES_AT}" != "unlimited" ]
then
    # Compute the remaining seconds before expiration in local time.
    REMAIN="$(${PYTHONBIN} - <<'PY'
import os
from datetime import datetime

expires_at = os.environ.get("EXPIRES_AT")
try:
    exp = datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%S")
    now = datetime.now()
    delta = int((exp - now).total_seconds())
    if delta < 0:
        delta = 0
    print(delta)
except Exception:
    print(0)
PY
)"

    if [ "${REMAIN}" -gt 0 ]
    then
        ( sleep "${REMAIN}";
          # Mark expiration for the next prompt.
          echo "Session expired for ${TARGETNAME} at ${EXPIRES_AT}." > "${EXPIRED_NOTICE}";
          # Kill the local session first (passhportd may be remote).
          kill -TERM -"${PID}" 2>/dev/null
          sleep 2
          kill -KILL -"${PID}" 2>/dev/null
          # Log the end of session in passhportd.
          if [ "${CERT}" == "/dev/null" ]
          then
              wget -qO - ${URL}connection/ssh/disconnect/${PID} &> /dev/null
          else
              wget --ca-certificate=${CERT} -qO - ${URL}connection/ssh/disconnect/${PID} &> /dev/null
          fi
        ) &
    else
        echo "Session expired for ${TARGETNAME} at ${EXPIRES_AT}." > "${EXPIRED_NOTICE}"
        kill -TERM -"${PID}" 2>/dev/null
        sleep 2
        kill -KILL -"${PID}" 2>/dev/null
        if [ "${CERT}" == "/dev/null" ]
        then
            wget -qO - ${URL}connection/ssh/disconnect/${PID} &> /dev/null
        else
            wget --ca-certificate=${CERT} -qO - ${URL}connection/ssh/disconnect/${PID} &> /dev/null
        fi
    fi
fi

###### SSH CONNECTION ########
script -q --timing=${FILELOG}.timing ${FILELOG} -c "ssh -t -p ${PORT} ${LOGIN}@${TARGET} ${OPTIONS}"
###### CALL PASSHPORTD TO END SESSION ######
if [ "${CERT}" == "/dev/null" ]
then
    wget -qO - ${URL}connection/ssh/endsession/${PID} &> /dev/null
    wget -qO - ${URL}target/changepassword/${TARGETNAME} &> /dev/null
else
    wget --ca-certificate=${CERT} -qO - ${URL}connection/ssh/endsession/${PID} &> /dev/null
    wget --ca-certificate=${CERT} -qO - ${URL}target/changepassword/${TARGETNAME} &> /dev/null
fi

# Launch PaSSHport with the same user after the connection
# If it's a direct connection, we don't connect again
if [ "${KEEPCONNECT}" -eq "1" ] && [ -z "${SSH_ORIGINAL_COMMAND}" ] && [ -z "${PASSHPORT_TARGET}" ]
then
    exec ${PYTHONBIN} ${PASSHPORTBIN} ${USERNAME} 
fi
