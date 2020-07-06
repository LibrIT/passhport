#!/bin/bash
###############################################################################
#                                                                             #
# Licensed under GPLv3.                                                       #
#                                                                             #
# Used to save all passhport data from webui installed on same machhine.      #
#                                                                             #
###############################################################################


HD="/home/passhport"
DATE="$(date +%Y%m%d%H%M%S)"
DIR_TO_SAVE=".ssh passhport.sql passhport_config certs"
OUTPUT_FILE="passhport_${DATE}.tar.gz"

# 0 remove old saves
#or not?
echo "SAVING..."

# 1. save the database
cd ${HD}
pg_dump passhport > passhport.sql

# Copy configuration
cp -r /etc/passhport passhport_config
cp -r /etc/apache2/sites-available/passhweb.conf passhport_config/

# 2. save in an archive
tar czf ${OUTPUT_FILE} ${DIR_TO_SAVE} &> /dev/null


if [[ $? == 0 ]]
then
    # 3. return the file name
    echo ${OUTPUT_FILE}
else
    echo "Error on save. Please contact support"
fi

# 4. rm temp data
rm -rf passhport_config
rm -rf passhport.sql

