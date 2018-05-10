# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

import psutil, re
from datetime import datetime, timedelta, date
from app import app
from .views_mod import user, target, usergroup, targetgroup, logentry
from .models_mod import logentry
from .models_mod import user
from .models_mod import target



@app.route("/")
def imalive():
    return """passhportd is running, gratz!\n"""


@app.route("/reporting/daily")
def dailyreport():
    """Return text containing previous day connections"""
    output = "Yesterday connections:\n"
    # 1. Define yesterday date at midnight.
    yesterday = date.today() - timedelta(1)
    yesterday = yesterday.strftime('%Y%m%d') + "T000000"

    # 2. Select logs entries from yesterday
    query = logentry.Logentry.query.filter(
            logentry.Logentry.connectiondate >= yesterday).all()

    for row in query:
        output = output + row.connectiondate + ": " + \
                 row.user[0].show_name() + \
                 " -> " + row.target[0].show_name() + "\n"

    if output == "Yesterday connections:\n":
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


def hours_minutes(td):
    """Takes timedelta object and express it in hours/min"""
    return str((td.days * 24) + (td.seconds//3600)) + "h" + \
           str((td.seconds//60)%60)


@app.route("/connection/ssh/current")
def currentsshconnections():
    """Return a json presenting the current ssh connections associated 
       to their PID"""
    output        = "[ "
    pythonexec    = "/home/passhport/passhport-run-env/bin/python3"
    passhportexec = "/home/passhport/passhport/passhport/passhport" 
    
    logs = logentry.Logentry.query.all()
    procs = [proc for proc in psutil.process_iter() \
             if proc.username() == "passhport"]

    for proc in procs:
        if pythonexec in proc.cmdline() and passhportexec in proc.cmdline():
            # It's a passhport process, his child is a ssh connection
            if len(proc.children()) == 1:
                sshcmd = proc.children()[0].cmdline()
                # Check if it's a ssh connection
                if [s for s in sshcmd if "script -q --timing=" in s]:
                    connection = [log for log in logs \
                              if log.logfilename in sshcmd[2]][-1]

                    cdate = datetime.strptime(connection.connectiondate,
                                             '%Y%m%dT%H%M%S')
                    duration = datetime.now() - cdate
                    # output json formated
                    output = output + \
                             '{"Email" : "' + \
                             connection.user[0].show_name() + '",' + \
                             '"Target" : "' + \
                             connection.target[0].show_name() + '",' + \
                             '"PID" : "' + str(proc.pid) + '",' + \
                             '"Date" : "' + \
                             hours_minutes(duration) + '"},' 
                             
    return output[:-1] + "]"


@app.route("/connection/ssh/disconnect/<pid>")
def sshdisconnection(pid):
    """Kill the pid"""
    parent = psutil.Process(int(pid))
    for child in parent.children(): 
        child.kill()
    parent.kill()
    return "Done"
