#!/bin/bash
########
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
########

# This script is used when you want to have a master-master PostGreSQL cluster.
# We use bucardo (https://bucardo.org) to have this master-master cluster, but
# the problem is that postgres won't update its "in memory" last available ID
# of the tables. So if you add a target on the first master, bucardo will 
# update the second master accordingly. The problem is that if you now try to 
# add a target on the second server, the postgres server will try to add an
# entry with the same ID sequence, because it doesn't know that it has been 
# updated (yes… that is a strange behavior). The workarround is to set 
# different initial sequence number and increment. This script does that.

# Usage : postgres-set-seq-id.sh TOTAL_SERVER_IN_CLUSTER LOCAL_SERVER_NUMBER

TOTAL_SERVER=$1
SERVER_NUMBER=$2
if [ -z "${TOTAL_SERVER}" ]
then
	echo -n "How many serveur to get replication ? : "
	read TOTAL_SERVER
fi
if [ -z "${SERVER_NUMBER}" ]
then
	echo -n "What is the number of this server ? (first server is 1, second server is 2, etc…) : "
	read SERVER_NUMBER
fi

for TABLE in exttargetaccess logentry passentry target targetgroup user usergroup
do
	LAST_ID=`psql passhport -qAtX -c "SELECT * FROM \"${TABLE}\" ORDER BY id"  | tail -n 1 | cut -d'|' -f 1`
	if [ -z "${LAST_ID}" ]
	then
		LAST_ID=0
	fi
	AVAILABLE_NEXT_ID=`expr ${LAST_ID} \+ 1`
	NEXT_ID_FOUND=1
	while [ $NEXT_ID_FOUND -ne 0 ]
	do
		NEXT_ID_FOUND=`expr \( ${SERVER_NUMBER} \+ ${AVAILABLE_NEXT_ID} \) % ${TOTAL_SERVER}`
		if [ $NEXT_ID_FOUND -ne 0 ]
		then
			AVAILABLE_NEXT_ID=`expr ${AVAILABLE_NEXT_ID} \+ 1`
		fi
	done
	#echo "psql passhport -c \"ALTER SEQUENCE ${TABLE}_id_seq RESTART ${AVAILABLE_NEXT_ID} INCREMENT ${TOTAL_SERVER};\""
	psql passhport -c "ALTER SEQUENCE ${TABLE}_id_seq RESTART ${AVAILABLE_NEXT_ID} INCREMENT ${TOTAL_SERVER};"
done
