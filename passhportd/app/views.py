# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from datetime import datetime, timedelta, date
from app import app
from .views_mod import user, target, usergroup, targetgroup, logentry
from .models_mod import logentry as log
from .models_mod import user



@app.route("/")
def imalive():
    return """passhportd is running, gratz!\n"""


@app.route("/reporting/daily")
def dailyreport():
    """Return text containing previous day connections"""
    output = ""
    # 1. Define yesterday date at midnight.
    yesterday = date.today() - timedelta(1)
    yesterday = yesterday.strftime('%Y%m%d') + "T000000"

    # 2. Select logs entries from yesterday
    query = log.Logentry.query.filter(
            log.Logentry.connectiondate >= yesterday).all()

    for row in query:
        output = output + row.connectiondate + ": " + \
                 row.user[0].show_name() + \
                 " -> " + row.target[0].show_name() + "\n"

    if output == "":
        return "No Log yesterday."

    return output

@app.route("/reporting/weekly/<weeksnb>")
def weeklyreport(weeksnb):
    """Return text contening unused servers and unused accounts"""
    output = "This users haven't used their account in weeks:\n"
    
    #1. Select all users and try them on last week logs
    users = user.User.query.all()

    neverused = [u for u in users if u.lastconnection() == -1]
    notusedlastweek = [u for u in users if u.lastconnection() > 7]

    for u in notusedlastweek:
        output = output + u.show_name() + " : " + \
                 str(int(u.lastconnection()/7) ) + "\n"

    output = output + "\nThis accounts have never been used: " + \
             ", ".join([u.show_name() for u in neverused]) + "\n"

     #2. Same for servers



    return output
