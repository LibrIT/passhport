#!/bin/bash
#Add new configuration field
grep "DB_SESSIONS_TO" /etc/passhport/passhportd.ini > /dev/null || echo "DB_SESSIONS_TO = 12" >> /etc/passhport/passhportd.ini
