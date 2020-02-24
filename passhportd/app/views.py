# -*-coding:Utf-8 -*-
import psutil
import re
import subprocess
import os
import config
from datetime import datetime
from datetime import timedelta
from datetime import date
from app import app
from app import db
from .views_mod import user
from .views_mod import target
from .views_mod import usergroup
from .views_mod import targetgroup
from .views_mod import logentry
from .views_mod import utils
from .models_mod import logentry
from .models_mod import user
from .models_mod import target
from .models_mod import exttargetaccess
from flask import request
from flask import stream_with_context
from flask import  Response
from tabulate import tabulate

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
    headers = ["Start", "End", "User name", "Target name", "Target hostname", "Command"] #[SESSION]

    # First we create an ordonned list with the 5 columns
    olist=[]
    for row in query:
        olist.append([row.connectiondate[9:11] + ":" + \
                      row.connectiondate[11:13], # Start date
                      row.show_endsessiondate()[9:11] + ":" + \
                      row.show_endsessiondate()[11:13], # End date
                      row.show_username(), # User name
                      row.show_targetname(), # Target name
                      row.show_targethostname(), #Target hostname
                      row.connectioncmd]) # Command

    # Tabulate construct the table from this list
    output = tabulate(olist, headers = headers, tablefmt="html")
    # Add some decorations
    output = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">' + \
             '<html>' +  \
             '<head>' + \
             '<meta http-equiv=3D"Content-Type" content="text/html; charset=3Diso-8859-1">' + \
             '<style>table, th, td { border: 1px solid black; border-collapse: collapse; }\n' + \
             'th, td { padding: 5px; } </style>' + \
             '</head>' + \
             '<body>' + \
             '<center>' + \
             '<h1>PaSSHport Daily report</h1>' + output + \
             '</center>' + \
             '</body>' + \
             '</html>' 
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
    lentries = logentry.Logentry.query.filter(db.and_(
               logentry.Logentry.endsessiondate == None,
	       logentry.Logentry.target != None,
	       logentry.Logentry.user != None)).all()

    if not lentries:
        return "[]"

    output = "[ "

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


@app.route("/connection/db/current")
def currentdbconnections():
    """Return a json presenting the current database connections associated 
       to their PID"""
    now = datetime.now()
    access = exttargetaccess.Exttargetaccess.query.filter(db.and_(
               exttargetaccess.Exttargetaccess.stopdate >= str(now),
               exttargetaccess.Exttargetaccess.proxy_pid != 0 )).all()

    if not access:
        return "[]"

    output = "[ "

    for entry in access:
        duration = now - datetime.strptime(entry.startdate,'%Y-%m-%d %H:%M:%S.%f')
        output = output + \
                '{"Email" : "' + \
                 entry.show_username() + '",' + \
                 '"Target" : "' + \
                 entry.show_targetname() + '",' + \
                 '"PID" : "' + str(entry.proxy_pid) + '",' + \
                 '"Date" : "' + hours_minutes(duration) + '"},'
                             
    return output[:-1] + "]"


@app.route("/connection/ssh/current/killbiglog")
def currecntsshconnectionskillbiglog():
    """Kill the actives sessions whith log files too big"""
    # Request to check only the connections on this node
    lentries = logentry.Logentry.query.filter(db.and_(
               logentry.Logentry.endsessiondate == None,
               logentry.Logentry.target != None,
               logentry.Logentry.logfilename.like(
                                    config.NODE_NAME + '-%'),
               logentry.Logentry.connectioncmd.like('%ssh%'),
	           logentry.Logentry.user != None)).all()

    killedpid = ""
    confmaxsize = int(config.MAXLOGSIZE)*1024*1024

    if lentries:
        for entry in lentries:
            maxsize = confmaxsize
            # First we check if the user has a specific file size
            specsize = entry.user[0].show_logfilesize()
            if specsize != 0: # 0 means unlimited
                if specsize != "Default":
                    maxsize = int(specsize)*1024*1024 # we set the maxsize for this user
                # Now we check this size against the actual file
                try:
                    logsize = os.path.getsize(entry.logfilepath + entry.logfilename)
                except:
                    logsize = 0
                    print("Error getting info on this file" + entry.logfilename)

                if logsize > maxsize:
                    sshdisconnect(entry.pid)
                    killedpid = str(entry.pid) + " " + killedpid

    return "Killed PIDs: " + killedpid


def is_pid_running(pid):
    """Check if the process is still running"""
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


@app.route("/connection/ssh/checkandterminate")
def checkandterminatesshsession():
    """Check all the connections and close those without a process runing"""
    lentries = logentry.Logentry.query.filter(db.and_(
               logentry.Logentry.endsessiondate == None,
               logentry.Logentry.logfilename.like(
                                   config.NODE_NAME + '-%'))).all()
    
    app.logger.error(lentries)
    if not lentries:
        return "No active connection."

    for entry in lentries:
        if not is_pid_running(entry.pid):
            endsshsession(entry.pid)
            app.logger.warning("Orphan connection with PID:" + \
                        str(entry.pid) + ". Now closed in the logentry.")

    return "Active connections: check done."


@app.route("/connection/ssh/endsession/")
def oldentriesendsession():
    """Force old entries without PID to be noted as closed"""
    isodate    = datetime.now().isoformat().replace(":",""). \
                 replace("-","").split('.')[0]
    lentries = logentry.Logentry.query.filter(
             logentry.Logentry.pid is None).all()

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
    # taking the last connection with this PID (the most recent)
    lentry = logentry.Logentry.query.filter(db.and_(
             logentry.Logentry.pid == int(pid),
             logentry.Logentry.endsessiondate == None)).first()

    if not lentry:
        return "Error: no logentry with this PID"

    lentry.setenddate(isodate)

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return utils.response('ERROR: "' + name + '" -> ' + e.message, 409)

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
            app.logger.warning("Impossible to kill: no such process with PID " + str(pid))

    return "Done"


########################
#### FILES DOWNLOAD ####
@app.route("/prepdownload", methods=["POST"])
def prepdownload():
    """Check if the file is a regular avalaible file before any transfer"""
    targetname = request.form["target"]
    filename = request.form["filename"]
    player = None
    if "player" in request.form:
        player = request.form["player"]

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
    if player:
        #In case of player, we need to create a totally different command
        # players are target not registred in passhport but accessible
        # No specific port, no option .. limited.
        # You need the key in the right place as shown below
        txtcommand = "ssh -oBatchMode=yes -i /home/passhport/players_keys/" + \
                     targetname.split("@",1)[0] + "/.ssh/" + \
                     targetname.split("@",1)[0] + " " + \
                     player + " ls " + filename +  " | wc -l"

    command    = [ elt for elt in txtcommand.split(" ")]
    try:
        p = subprocess.check_output(command)
    except:
        return utils.response("ERROR: can't connect", 404)

    if str(p.decode()) != "1\n":
        return utils.response("ERROR: file cannot be found", 404)
    return utils.response("OK", 200)


@app.route("/download", methods=["POST"])
def directdownload():
    """Return a stream containing file from target"""
    targetname = request.form["target"]
    filename = request.form["filename"]
    player = None
    if "player" in request.form:
        player = request.form["player"]

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
    if player:
        # Check previous comment about players
        txtcommand = "scp -i /home/passhport/players_keys/" + \
                     targetname.split("@",1)[0] + "/.ssh/" + \
                     targetname.split("@",1)[0] + " " + \
                     player + ":" + filename +  " " + \
                      "/dev/stdout"

    command    = [ elt for elt in txtcommand.split(" ")]
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
    except:
        return utils.response("ERROR: can't connect", 404)

    return Response(stream_with_context(p.stdout))
