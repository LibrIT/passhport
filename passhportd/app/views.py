# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from datetime import datetime, timedelta, date
from app import app
from .views_mod import user, target, usergroup, targetgroup, logentry
from .models_mod import logentry as log
from .models_mod import user
from .models_mod import target



@app.route("/")
def imalive():
    return """passhportd is running, gratz!\n"""


@app.route("/reporting/daily")
def dailyreport():
    """Return text containing previous day connections"""
    output = "This users didn't connect this week:\n"
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

    if output == "This users didn't connect this week:\n":
        return "No Log yesterday."

    return output

@app.route("/reporting/weekly/<weeksnb>")
def weeklyreport(weeksnb=4):
    """Return text contening unused servers and unused accounts"""
    output = "This users haven't used their account in weeks:\n"
    
    #1. Select all users and try them on last week logs
    users = user.User.query.all()

    neverused = [u for u in users if u.dayssinceconnection() == -1]
    notusedlastweek = [u for u in users if u.dayssinceconnection() > 7]

    for u in notusedlastweek:
        output = output + u.show_name() + " -> " + \
                 str(int(u.dayssinceconnection()/7) ) + "\n"

    output = output + "\nThis accounts have never been used:\n" + \
             ", ".join([u.show_name() for u in neverused]) + "\n"

    #2. Same for servers
    output = output + "No one connected this targets in weeks:\n"
    daysnotused = int(weeksnb * 7)
    targets = target.Target.query.all()

    neverused = [t for t in targets if t.dayssinceconnection() == -1]
    notused = [t for t in targets if t.dayssinceconnection() >= daysnotused]
    for t in notused:
        output = output + t.show_name() + " -> " + \
                 str(int(t.dayssincelastconnection()/7) ) + "\n"

    output = output + "\nThis targets has never been used through passhport:\n"
    output = output + ", ".join([t.show_name() for t in neverused])

    return output
