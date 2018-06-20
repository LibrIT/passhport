#! /bin/bash
wget --no-check-certificate -qO - https://localhost:5000/reporting/weekly/4 | /usr/bin/mail -s "PaSSHport weekly report" user@example.com

