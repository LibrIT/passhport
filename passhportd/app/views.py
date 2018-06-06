# -*-coding:Utf-8 -*-
import psutil, re, subprocess
from datetime import datetime, timedelta, date
from app import app, db
from .views_mod import user, target, usergroup, targetgroup, logentry, utils
from .models_mod import logentry
from .models_mod import user
from .models_mod import target
from flask import request, stream_with_context, Response


@app.route("/")
def imalive():
    return """passhportd is running, gratz!\n"""

#########################
#### EMAIL REPORTING ####
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
    minutes = str((td.seconds//60)%60)
    if len(minutes) == 1:
        minutes = "0" + minutes

    return str((td.days * 24) + (td.seconds//3600)) + "h" + \
           minutes + "min"

########################################
#### Current connections management ####
@app.route("/connection/ssh/current")
def currentsshconnections():
    """Return a json presenting the current ssh connections associated 
       to their PID"""

    lentries = logentry.Logentry.query.filter(
               logentry.Logentry.endsessiondate == None).all()

    if not lentries:
        return "[]"

    output        = "[ "
    for entry in lentries:
        cdate = datetime.strptime(entry.connectiondate,
                                             '%Y%m%dT%H%M%S')
        duration = datetime.now() - cdate
        output = output + \
                '{"Email" : "' + \
                 entry.user[0].show_name() + '",' + \
                 '"Target" : "' + \
                 entry.target[0].show_name() + '",' + \
                 '"PID" : "' + str(entry.pid) + '",' + \
                 '"Date" : "' + hours_minutes(duration) + '"},'
                             
    return output[:-1] + "]"


@app.route("/connection/ssh/checkandterminate")
def checkandterminatesshsession():
    """Check all the connections and close those without a process runing"""
    isodate    = datetime.now().isoformat().replace(":",""). \
                 replace("-","").split('.')[0]
    lentries = logentry.Logentry.query.filter(
             logentry.Logentry.endsessiondate == None).all()

    if not lentries:
        return "No active connection."

    for entry in lentries:
        try:
            parent = psutil.Process(entry.pid)
        except Exception as E:
            if type(E) == psutil.NoSuchProcess:
                endsshsession(entry.pid)
                print("Orphan connection with PID:" + str(entry.pid) + \
                        ". Now closed in the logentry.")

    return "Active connections: check done."


@app.route("/connection/ssh/endsession/")
def oldentriesendsession():
    """Force old entries without PID to be noted as closed"""
    isodate    = datetime.now().isoformat().replace(":",""). \
                 replace("-","").split('.')[0]
    lentries = logentry.Logentry.query.filter(
             logentry.Logentry.pid == None).all()

    if not lentries:
        return "Error: no logentry without PID"

    for entry in lentries:
        if entry.endsessiondate:
            return "Already ended"
        entry.setenddate(isodate)

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + e.message, 409)

    return "Done"


@app.route("/connection/ssh/disconnect/<pid>")
def sshdisconnect(pid):
    """Check if the session is well terminated and log infos about the end"""
    # Be sure the session is closed or forceclose
    sshdisconnection(pid)
    # Validate logs
    return endsshsession(pid)


@app.route("/connection/ssh/endsession/<pid>")
def endsshsession(pid):
    """log infos about the end of a session"""
    # modify the associated Logentry to signal the end date
    isodate    = datetime.now().isoformat().replace(":",""). \
                 replace("-","").split('.')[0]
    lentry = logentry.Logentry.query.filter(
             logentry.Logentry.pid == int(pid)).first()

    if not lentry:
        return "Error: no logentry with this PID"

    if lentry.endsessiondate:
        return "Already ended"
    lentry.setenddate(isodate)

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + e.message, 409)

    #At last change the root password if needed
    lentry.target[0].changepass(isodate)

    return "Done"


def sshdisconnection(pid):
    """Kill the pid no matter what"""
    try:
        parent = psutil.Process(int(pid))
        for child in parent.children(): 
            child.kill()
        parent.kill()

    except Exception as E:
        if type(E) == psutil.NoSuchProcess:
            print("Impossible to kill: no such process with PID " + str(pid))

    return "Done"


########################
#### FILES DOWNLOAD ####
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

