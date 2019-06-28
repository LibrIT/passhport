#! /bin/bash

function create_targetgroups(){
	passhport-admin targetgroup create network-switches --comment "Ensemble des switches de l'entreprise"
	passhport-admin targetgroup create network-access-points --comment "Ensemble des Points d'Accès WiFI"
	passhport-admin targetgroup create network-routers --comment "Tous les routeurs de l'entreprise"
	passhport-admin targetgroup create network-targets --comment "Tous les périphériques réseau de l'entreprise"
	passhport-admin targetgroup create Windows-servers --comment "Tous les serveurs Windows accessibles en SSH (core)"
	passhport-admin targetgroup create Linux-servers --comment "Tous les serveurs Linux (redhat/debian/etc) de l'entreprise"
	passhport-admin targetgroup create ALL-TARGETS --comment "TOUTES LES TARGETS - RÉSERVÉ AUX SUPERS ADMIN"
}


function generate_targets(){
	OCTET_D=2
	OCTET_C=1
	OCTET_B=1
	for TARGET_NAME_PREFIX in SRV-LNX NET-ROUTER NET-SWITCH NET-AP SRV-WIN
	do
		TARGET_ID=0
		while [ ${TARGET_ID} -lt 500 ]
		do
			TARGET_ID=`expr ${TARGET_ID} \+ 1`
			ID_LENGTH=${#TARGET_ID}
			if [ ${#TARGET_ID} -lt 2 ]
			then
				TARGET_NAME_SUFFIX="000${TARGET_ID}"
			elif [ ${#TARGET_ID} -lt 3 ]
			then
				TARGET_NAME_SUFFIX="00${TARGET_ID}"
			elif [ ${#TARGET_ID} -lt 4 ]
			then
				TARGET_NAME_SUFFIX="0${TARGET_ID}"
			else
				 TARGET_NAME_SUFFIX="${TARGET_ID}"
			fi
			TARGET_NAME="${TARGET_NAME_PREFIX}-${TARGET_NAME_SUFFIX}"

			if [ ${OCTET_D} -lt 254 ] 
			then
				OCTET_D=`expr ${OCTET_D} \+ 1`
			elif [ ${OCTET_D} -ge 254 ] && [ ${OCTET_C} -lt 254 ]
			then
				OCTET_D=1
				OCTET_C=`expr ${OCTET_C} \+ 1`
			elif [ ${OCTET_D} -ge 254 ] && [ ${OCTET_C} -ge 254 ]
			then
				OCTET_D=1
				OCTET_C=1
				OCTET_B=`expr ${OCTET_B} \+ 1`
			fi
			passhport-admin target create "${TARGET_NAME}" "127.${OCTET_B}.${OCTET_C}.${OCTET_D}"
			if [ "${TARGET_NAME_PREFIX}" == "SRV-LNX" ]
			then
				passhport-admin targetgroup addtarget "${TARGET_NAME}" "Linux-servers"
			elif [ "${TARGET_NAME_PREFIX}" == "SRV-WIN" ]
			then
				passhport-admin targetgroup addtarget "${TARGET_NAME}" "Windows-servers"
			elif [ "${TARGET_NAME_PREFIX}" == "NET-SWITCH" ]
			then
				passhport-admin targetgroup addtarget "${TARGET_NAME}" "network-switches"
				passhport-admin targetgroup addtarget "${TARGET_NAME}" "network-targets"
			elif [ "${TARGET_NAME_PREFIX}" == "NET-AP" ]
			then
				passhport-admin targetgroup addtarget "${TARGET_NAME}" "network-access-points"
				passhport-admin targetgroup addtarget "${TARGET_NAME}" "network-targets"
			elif [ "${TARGET_NAME_PREFIX}" == "NET-ROUTER" ]
			then
				passhport-admin targetgroup addtarget "${TARGET_NAME}" "network-routers"
				passhport-admin targetgroup addtarget "${TARGET_NAME}" "network-targets"
			fi
			passhport-admin targetgroup addtarget "${TARGET_NAME}" "ALL-TARGETS"
			echo "${TARGET_NAME} created."
		done
	done
}

function create_usergroups(){
	passhport-admin usergroup create linux-admins --comment "Ensembles des administrateurs Linux/Unix"
	passhport-admin usergroup create windows-admins --comment "Ensembles des administrateurs Linux/Unix"
	passhport-admin usergroup create network-admins --comment "Ensembles des administrateurs Linux/Unix"
	passhport-admin usergroup create network-switches-admins --comment "Ensembles des administrateurs Linux/Unix"
	passhport-admin usergroup create network-access-points-admins --comment "Ensembles des administrateurs Linux/Unix"
	passhport-admin usergroup create network-routers-admins --comment "Ensembles des administrateurs Linux/Unix"
}

function generate_users(){
	TYPES_ADMIN[0]="LNX_ADMIN"
	TYPES_ADMIN[1]="WIN_ADMIN"
	TYPES_ADMIN[2]="NET_ADMIN"
	TYPES_ADMIN[3]="NET_SW_ADMIN"
	TYPES_ADMIN[4]="NET_AP_ADMIN"
	TYPES_ADMIN[5]="NET_RO_ADMIN"
	NUMBER_OF_USERS=500
	while [ ${NUMBER_OF_USERS} -ge 0 ]
	do
		USER_INFO=`rig`
		USER_FULL_NAME=`echo "${USER_INFO}" | head -n 1`
		USER_USERNAME=`echo -n ${USER_FULL_NAME} | tr '[:upper:]' '[:lower:]' | tr ' ' '.'`
		USER_MAIL=`echo -n ${USER_USERNAME}@passhport.com`
		USER_COMMENT="${USER_FULL_NAME} - `echo -n ${USER_INFO} | tail -n 3`"
		KEY_FILE="/home/demo-passhport/users-keys/id_rsa-`echo -n ${USER_FULL_NAME} | tr '[:upper:]' '[:lower:]' | tr ' ' '_'`"
		PUB_KEY_FILE="${KEY_FILE}.pub"
		ssh-keygen -q -N "" -b 1024 -t rsa -f "${KEY_FILE}"
		PUB_KEY_STRING=`cat "${PUB_KEY_FILE}"`
		passhport-admin user create "${USER_MAIL}" "${PUB_KEY_STRING}" --comment "${USER_COMMENT}"
		NBR_TYPES_ADMIN=${#TYPES_ADMIN[@]}
		INDEX_TYPES_ADMIN_RANDOM=$(($RANDOM % ${NBR_TYPES_ADMIN}))
		USER_TYPE_ADMIN=${TYPES_ADMIN[${INDEX_TYPES_ADMIN_RANDOM}]}
		if [ "${USER_TYPE_ADMIN}" == "LNX_ADMIN" ]
		then
			passhport-admin usergroup adduser "${USER_MAIL}" "linux-admins"
		elif [ "${USER_TYPE_ADMIN}" == "WIN_ADMIN" ]
		then
			passhport-admin usergroup adduser "${USER_MAIL}" "windows-admins"
		elif [ "${USER_TYPE_ADMIN}" == "NET_ADMIN" ]
		then
			passhport-admin usergroup adduser "${USER_MAIL}" "network-admins"
		elif [ "${USER_TYPE_ADMIN}" == "NET_SW_ADMIN" ]
		then
			passhport-admin usergroup adduser "${USER_MAIL}" "network-switches-admins"
		elif [ "${USER_TYPE_ADMIN}" == "NET_AP_ADMIN" ]
		then
			passhport-admin usergroup adduser "${USER_MAIL}" "network-access-points-admins"
		elif [ "${USER_TYPE_ADMIN}" == "NET_RO_ADMIN" ]
		then
			passhport-admin usergroup adduser "${USER_MAIL}" "network-routers-admins"
		fi
		echo "User number ${NUMBER_OF_USERS} created."
		NUMBER_OF_USERS=`expr ${NUMBER_OF_USERS} - 1`
	done
}

create_targetgroups
generate_targets
create_usergroups
generate_users
