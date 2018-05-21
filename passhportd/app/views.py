# -*-coding:Utf-8 -*-
import psutil, re, subprocess
from datetime import datetime, timedelta, date
from app import app
from .views_mod import user, target, usergroup, targetgroup, logentry, utils
from .models_mod import logentry
from .models_mod import user
from .models_mod import target
from flask import request, stream_with_context, Response


@app.route("/")
def imalive():
    return """passhportd is running, gratz!\n"""


@app.route("/reporting/daily")
def dailyreport():
    """Return text containing previous day connections"""
    # 1. Define yesterday date at midnight.
    yesterday = date.today() - timedelta(1)
    yesterday = yesterday.strftime('%Y%m%d') + "T000000"

    # 2. Select logs entries from yesterday
    query = logentry.Logentry.query.filter(
            logentry.Logentry.connectiondate >= yesterday).all()


    # 3. Format the output
    #First we create an ordonned list with the tree column
    olist=[]
    for row in query:
        olist.append({"user"   : row.user[0].show_name(),
                      "target" : row.target[0].show_name(), 
                      "date"   : row.connectiondate[9:11] + ":" + \
                                 row.connectiondate[11:13]})

    if len(olist) == 0:
        return "No connection logged yesterday."

    ucolsize=35
    tcolsize=20
    output = "Yesterday connections by user:\n"
    output = output + "Username" + " "*(ucolsize-len("Username")) + "\t"
    output = output + "Target" + " "*(tcolsize-len("Target")) + "\t"
    output = output + "Connection date\n"

    # Then obtain all usernames unicity and loop on usernames
    for user in set([log["user"] for log in olist]):
        firstline = True
        for row in [log for log in olist if log["user"] == user]:
            if firstline:
                output = output + user + " "*(ucolsize - len(user)) + "\t"
                firstline = False
            else:
                output = output + " "*(ucolsize) + "\t"
            output = output + row["target"] + \
                                " "*(tcolsize - len(row["target"])) + "\t" 
            output = output + row["date"] + "\n" 

    return output


@app.route("/reporting/weekly/<weeksnb>")
def weeklyreport(weeksnb=4):
    """Return text contening unused servers and unused accounts"""
    output = "This users haven't used their account in weeks:\n"
    output = output + "Username\tWeeks since last connection\n"
    
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
    output = output + "Target   \tWeeks since last connection\n"
    daysnotused = int(weeksnb * 7)
    targets = target.Target.query.all()

    neverused = [t for t in targets if t.dayssinceconnection() == -1]
    notused = [t for t in targets if t.dayssinceconnection() >= daysnotused]
    for t in notused:
        output = output + t.show_name() + "\t" + \
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


@app.route("/prepdownload", methods=["POST"])
def prepdownload():
    """Check if the file is a regular avalaible file before any transfer"""
    targetname = request.form["target"]
    filename = request.form["filename"]

    t = target.Target.query.filter_by(name=targetname).first()
    if t is None:
        return utils.response('ERROR: No target with this name', 417)

    # Prepare commands for connexion
    options = t.show_options().strip() + " "
    # Empty options breaks the command so we add " " to it
    if options != " ":
        options = " " + options 
    # midcmd = port option user@target
    midcmd = str(t.show_port()) + options + \
                 t.show_login() + "@" + t.show_hostname()

    txtcommand = "ssh -p" + midcmd + \
                 " ls " + filename +  " | wc -l"
    command    = [ elt for elt in txtcommand.split(" ")]
    p = subprocess.check_output(command)

    if str(p.decode()) != "1\n":
        return utils.response("ERROR: file cannot be found", 404)
    return utils.response("OK", 200)


@app.route("/download", methods=["POST"])
def directdownload():
    """Return a stream containing file from target"""
    targetname = request.form["target"]
    filename = request.form["filename"]

    t = target.Target.query.filter_by(name=targetname).first()
    if t is None:
        return utils.response('ERROR: No target with this name', 417)

    # Prepare commands for connexion
    options = t.show_options().strip() + " "
    # Empty options breaks the command so we add " " to it
    if options != " ":
        options = " " + options 
    # midcmd = port option user@target
    midcmd = str(t.show_port()) + options + \
                 t.show_login() + "@" + t.show_hostname()

    txtcommand = "scp -P" + midcmd + \
                 ":" + filename + " " + "/dev/stdout"
    command    = [ elt for elt in txtcommand.split(" ")]

    p = subprocess.Popen(command, stdout=subprocess.PIPE)

    return Response(stream_with_context(p.stdout))

