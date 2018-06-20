#! /bin/bash

(echo To:user@example.com; echo From:passhport@example.com; echo "Content-Type: text/html"; echo Subject: PaSSHport $(date  --date="7 days ago" +%y-%m) daily report; echo; wget --no-check-certificate -qO - https://passhportd.jcdecaux.com:5000/reporting/daily) | /usr/sbin/sendmail -t

