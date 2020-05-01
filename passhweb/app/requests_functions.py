#-*-coding:Utf-8 -*-

"""Contains functions which make requests to the passhportd server"""
import sys, locale, requests
from flask import jsonify
from app import app
import config

def get(path):
    """Send the GET request to the passhport server and print a result"""
    url = config.url_passhportd + path
    app.logger.info("==> Connection to passhportd: " + url)
    try:
        r = requests.get(url, verify=False)
    except requests.RequestException as e:
        app.logger.error("ERROR connecting to PaSSHportd")
        app.logger.error(e)
    else:
        if r.status_code == requests.codes.ok:
            return r.text
    
    return None


def post(path, data, author = None):
    """Send the POST request to the server and print a result"""
    url = config.url_passhportd + path
    app.logger.info("Connection to passhportd: " + url)

    # Add request author on data
    if author:
        data = data.copy()
        data["author"] = author


    try:
        r = requests.post(url, data = data, verify=False)
    except requests.exceptions.Timeout:
        app.logger.error("ERROR: Connection timed out." + \
                                            "Check your configuration.")
    except requests.exceptions.ConnectionError as e:
        app.logger.errror("ERROR: Connection error. " + \
                                  "Check your configuration.\n" + str(e))
    except requests.exceptions.TooManyRedirects:
        app.logger.error("ERROR: Too many redirects.")
    except requests.exceptions.RequestException as e:
        app.logger.error("Error: " + str(e))
    else:
        if r.status_code == requests.codes.ok:
            return r.text
        else:
            app.logger.error(r.text)

    return None


def proxypost(path, data):
    """Return a streaming object"""
    url = config.url_passhportd + path
    print("==> Connection to passhportd via stream: " + url)
    return requests.post(url, data = data, stream = True, verify=False)


def check_list(api_resp):
    """Check if the list is really a list or None and do a proper json"""
    if api_resp:
        # passhportd return a json, that we eval in dict
        return eval(str(api_resp).replace("\r",""))
    else:
        return None


def get_dict(element):
    """Return a list of existing element"""
    return check_list(get("api/" + element + "/list"))


def get_specific_dict(element, name):
    """Return a list of existing element accessible by name"""
    return check_list(get("api/" + element + "/list/" + name))


def get_attached(element, attached, name):
    """Return a list of attached user/target/targetgroup/usergroup"""
    return check_list(get("api/" + element + "/" + attached + "/" + name))


def get_element(element, name):
    """Return an element details"""
    return check_list(get("api/" + element + "/show/" + name))


def addrmelt(obj, elt, operation, data, author = None):
    """Remove or add an element from an object on passhportd via API""" 
    return post(obj + "/" + operation + elt, data, author)


def listeltlink(element, data):
    """Return a list of html links in str format created from data"""
    output = ""
    if not data:
        return "None"
    
    for obj in data[1:-1].replace("', ",",").replace("'","").split(","):
        link = "/edit/" + element + "/" + obj
        output = output + htmllink(link, obj) + ", "

    output = output[:-2]
    return output


### Datatables formatting ###
def htmllink(link, text):
    """Return a html formatted link"""
    return "<a href=\'" + link + "\'>" + text + "</a>"


def htmldelbutton(obj1, obj2):
    """Return html code for  delete button of obj1 from obj2"""
    return "<button id='deleteclose' type='button' " + \
           "class='deleteclose btn btn-block btn-danger' data-toggle=" + \
           "'tooltip' title='Remove " + obj1 + " from this " + obj2 +\
           "'>\\n" + \
           "<span id='butdelspan'>&times;</span>\\n" + \
           "</button>"


def htmlaskbutton(targetname, data):
    """Return html code for access ask button"""
    msg = "Click here to open a temporary access to this target"
    tooltip = "Create a temporary access for this computer"
    butclass = "btn-primary"
    if data:
        if targetname in data:
            msg = "Connect via " + data[targetname]["proxy_ip"] + \
                  " on port " + data[targetname]["proxy_port"] + \
                  " until " + data[targetname]["enddate"] 
            tooltip = "Close this connection"
            butclass = "btn-success"

    return "<button id='accessask' type='button' " + \
           "class='accessask btn btn-block " + butclass + "' data-toggle=" + \
           "'tooltip' title='"+ tooltip + "'" + \
           "'>\\n" + msg + "\\n" + \
           "</button>"


def htmldbcloseaccess(targetname, data, ishidden=True):
    """Return html code for closing opened access"""
    msg = "X"
    hidden = ""
    buttondef = "button id='accessclose' type='button' " + \
                "class='accessclose btn btn-block btn-danger' data-toggle=" + \
                "'tooltip' title='Close this access'"
    #TODO put this in a css
    if ishidden:
        hidden = " style='visibility: hidden'"
    if data:
        if targetname in data:
            return "<" + buttondef + ">\\n" + msg + "\\n" + \
                  "</button>"

    return "<" + buttondef + hidden + ">\\n" + msg + "\\n" + \
           "</button>"


def htmlclosebutton(targetname):
    """Return html code for closing opened access"""
    msg = "X"
    return "<button id='accessclose' type='button' " + \
           "class='accessclose btn btn-block btn-error' data-toggle=" + \
           "'tooltip' title='Close this access" + \
           "'>\\n" + msg + "\\n" + \
           "</button>"


def get_attached_datatable(element, attached, name):
    """Return a list of attached user/target/targetgroup/usergroup"""
    tocall = "get_attached" + attached + "_datatable"
    return getattr(sys.modules[__name__], tocall)(element , name)


def get_users_datatable():
    """Return a list compatible with datatable"""
    output = "{\"data\":[]}"
    r = get_dict("user")
    if r:
        output = '{"data":['
        for data in r:
            output = output + "\n["
            output = output + "\"" + \
                 htmllink("/edit/user/" + data["email"], data["email"]) + "\","
            output = output + "\""+ data["sshkeyhash"] + "\","
            output = output + "\""+ data["comment"] + "\""
            output = output + "],"
        output = output[:-1] + "]}"""

    return output


def get_users_select2():
    """Return a list compatible with select2"""
    output = "{\"results\":[]}"
    r = get_dict("user")
    if r:
        output = '{"results":['
        i = 1
        for data in r:
            output = output + "\n{"
            output = output + "\"id\": \"" + str(i) + "\",\n"
            output = output + "\"text\": \"" + data["email"] + "\"\n"
            output = output + "},\n"
            i = i + 1
        output = output[:-2] + "],\n"
        output = output + "\"pagination\": {\"more\": false}\n}"""

    return output


def get_player_datatable(name=None):
    """Return the list of the players accessible to the user "name" #jcd"""
    output = "{\"data\":[]}"
    if not name:
        return output

    # List all the players the user can access
    r =  get("user/access/" + name)
    print(r)
    if not r or len(r) == 0:
        return output
    players = [p for p in eval(r) if p[:3] == "jcd"]

    # List all the targets
    r = get_dict("target")
    if not r or len(r) == 0:
        return output
    
    output = '{"data":['
    # Get the players details by comparing the lists
    for target in r:
        if target["Name"] in players:
            output = output + "\n["
            output = output + "\"" + \
                 htmllink("/show/player/" + target["Name"], 
                          target["Name"]) + "\","
            output = output + "\""+ target["Comment"] + "\""
            output = output + "],"
    output = output[:-1] + "]}"
    return output


def get_targets_datatable():
    """Return a list compatible with datatable"""
    output = "{\"data\":[]}"
    r = get_dict("target")
    if r:
        output = '{"data":['
        for data in r:
            output = output + "\n["
            output = output + "\"" + \
                 htmllink("/edit/target/" + data["Name"], data["Name"]) + "\","
            output = output + "\""+ data["Hostname"] + "\","
            output = output + "\""+ data["Target type"] + "\","
            if data["Target type"] != "ssh":
                output = output + "\"-\","
            else:
                output = output + "\""+ data["Login"] + "\","
            output = output + "\""+ data["Port"] + "\","
            output = output + "\""+ data["Comment"] + "\""
            output = output + "],"
        output = output[:-1] + "]}"

    return output


def get_target_lastconnections_datatable(name):
    """Return a list of logfile compatible with datatable"""
    output = '{"data":[ '
    r = check_list(get("target/lastlog/" + name))
    if not r or r == []:
        return '{"data": ""}'

    for data in r:
        output = output + "\n["
        output = output + "\""+ dateisotohuman(r[data]["Start date"]) + "\","
        if r[data]["End date"] != "Connected":
            output = output + "\""+ dateisotohuman(r[data]["End date"]) + "\","
        else:
            output = output + "\"Still connected\","
        output = output + "\"" + \
                htmllink("/edit/user/" + r[data]["User"],  r[data]["User"]) + "\","
        output = output + "\""+ r[data]["Logfile"] + "\""
        output = output + "],"
    output = output[:-1] + "]}"

    return output


def get_accesstargets_datatable(name):
    """Return a list compatible with datatable"""
    output = '{"data":['
    r = get_specific_dict("accesstarget", name)
    if r == []:
        return '{"data": ""}'

    for data in r:
        output = output + "\n["
        output = output + "\"" + \
                 htmllink("/edit/target/" + data["Name"], data["Name"]) + "\","
        output = output + "\""+ data["Hostname"] + "\","
        output = output + "\""+ data["Lastconnection"] + "\""
        output = output + "],"
    output = output[:-1] + "]}"
    
    return output


def get_usergroups_datatable():
    """Return a list compatible with datatable"""
    output = "{\"data\":[]}"
    r = get_dict("usergroup")
    if r:
        output = '{"data":['
        for data in r:
            output = output + "\n["
            output = output + "\"" + \
                     htmllink("/edit/usergroup/" + data["Name"], data["Name"]) + "\","
            output = output + "\""+ data["Comment"] + "\""
            output = output + "],"
        output = output[:-1] + "]}"
    

    return output


def get_targetgroups_datatable():
    """Return a list compatible with datatable"""
    output = "{\"data\":[]}"
    r = get_dict("targetgroup")
    if r:
        output = '{"data":['
        for data in r:
            output = output + "\n["
            output = output + "\"" + \
                     htmllink("/edit/targetgroup/" + data["Name"], data["Name"]) + "\","
            output = output + "\""+ data["Comment"] + "\""
            output = output + "],"
        output = output[:-1] + "]}"

    return output


def get_attachedmanager_datatable(element, name):
    """Return a attached list compatible with datatable"""
    output = "{\"data\":[]}"
    r = get_attached(element, "manager", name)
    if r:
        output = '{"data":['
        for data in r:
            output = output + "\n["
            output = output + "\"" + \
                     htmllink("/edit/user/" + data["Name"], data["Name"]) + "\","
            output = output + "\""+ data["Comment"] + "\","
            output = output + "\""+ htmldelbutton("user", "target") + "\""
            output = output + "],"
        output = output[:-1] + "]}"""

    return output


def get_attachedusers_datatable(element, name):
    """Return a attached list compatible with datatable"""
    output = "{\"data\":[]}"
    r = get_attached(element, "user", name)
    if r:
        output = '{"data":['
        for data in r:
            output = output + "\n["
            output = output + "\"" + \
                     htmllink("/edit/user/" + data["Name"], data["Name"]) + "\","
            output = output + "\""+ data["Comment"] + "\","
            output = output + "\""+ htmldelbutton("user", "target") + "\""
            output = output + "],"
        output = output[:-1] + "]}"""

    return output


def get_attachedusergroups_datatable(element, name):
    """Return a attached usergroup list compatible with datatable"""
    output = "{\"data\":[]}"
    r = get_attached(element , "usergroup", name)
    if r:
        output = '{"data":['
        for data in r:
            output = output + "\n["
            output = output + "\"" + \
                     htmllink("/edit/usergroup/" + \
                     data["Name"], data["Name"]) + "\","
            output = output + "\""+ data["Comment"] + "\","
            output = output + "\""+ htmldelbutton("usergroup", "target") + "\""
            output = output + "],"
        output = output[:-1] + "]}"""

    return output


def get_attachedtargets_datatable(element, name):
    """Return a attached target list compatible with datatable"""
    output = "{\"data\":[]}"
    r = get_attached(element , "target", name)
    if r:
        output = '{"data":['
        for data in r:
            output = output + "\n["
            output = output + "\"" + \
                     htmllink("/edit/target/" + \
                     data["Name"], data["Name"]) + "\","
            output = output + "\""+ data["Comment"] + "\","
            output = output + "\""+ htmldelbutton("target", "target") + "\""
            output = output + "],"
        output = output[:-1] + "]}"""

    return output


def get_attachedtargetgroups_datatable(element, name):
    """Return a attached targetgroup list compatible with datatable"""
    output = "{\"data\":[]}"
    r = get_attached(element , "targetgroup", name)
    if r:
        output = '{"data":['
        for data in r:
            output = output + "\n["
            output = output + "\"" + \
                     htmllink("/edit/targetgroup/" + \
                     data["Name"], data["Name"]) + "\","
            output = output + "\""+ data["Comment"] + "\","
            output = output + "\""+ \
                     htmldelbutton("targetgroup", "target") + "\""
            output = output + "],"
        output = output[:-1] + "]}"""

    return output


def get_current_ssh_connections():
    """Return a datatable compatible list of current ssh connections"""
    output = "{\"data\":[]}"
    r = check_list(get("connection/ssh/current"))
    if r:
        output = '{"data":['
        for data in r:
            output = output + "\n["
            output = output + "\"" + data["Date"] + "\","
            output = output + "\"" + \
                     htmllink("/edit/user/" + data["Email"], data["Email"]) + "\","
            output = output + "\"" + \
                     htmllink("/edit/target/" + \
                     data["Target"], data["Target"]) + "\","
            output = output + "\"" + data["PID"] + "\","
            output = output + "\""+ htmldelbutton("user", "ssh connection") + "\""
            output = output + "],"
        output = output[:-1] + "]}"""

    return output


def get_current_db_connections():
    """Return a datatable compatible list of current db connections"""
    output = "{\"data\":[]}"
    r = check_list(get("connection/db/current"))
    if r:
        output = '{"data":['
        for data in r:
            output = output + "\n["
            output = output + "\"" + data["Date"] + "\","
            output = output + "\"" + \
                     htmllink("/edit/user/" + data["Email"], 
                                         data["Email"]) + "\","
            output = output + "\"" + \
                     htmllink("/edit/target/" + \
                     data["Target"], data["Target"]) + "\","
            output = output + "\"" + data["PID"] + "\","
            output = output + "\""+ htmldbcloseaccess("user",
                                         "db connection", False) + "\""
            output = output + "],"
        output = output[:-1] + "]}"""

    return output


def get_accessible_database_datatable(user):
    """Return a datatable compatible list of current user accessible DB"""
    output = "{\"data\":[]}"
    r = check_list(get("api/target/list/" + user))
    useraccess = check_list(get("api/target/openedaccess/" + user))
    if r:
        output = '{"data":['
        for data in r:
            output = output + "\n["
            output = output + "\"" + \
                 htmllink("/edit/target/" + data["Name"], data["Name"]) + "\","
            output = output + "\""+ data["Hostname"] + "\","
            output = output + "\""+ data["Target type"] + "\","
            output = output + "\"" + htmlaskbutton(data["Name"], useraccess) + "\","
            output = output + "\"" + \
                 htmldbcloseaccess(data["Name"], useraccess) + "\""
            output = output + "],"
        output = output[:-1] + "]}"

    return output


def get_password_datatable(targetname):
    """Return a datatable compatible list of target passwords"""
    output = "{\"data\":[]}"
    r = check_list(get("target/getpassword/" + targetname))
    if r:
        output = '{"data":['
        for data in r:
            output = output + "\n["
            output = output + "\"" + dateisotohuman(data["date"]) + "\","
            output = output + "\"" + data["password"] + "\""
            output = output + "],"
        output = output[:-1] + "]}"""

    return output

def dateisotohuman(d):
    """Takes a datein ISO format like 20180225T145522 and return it
    in human readable format"""
    return  d[0:4] + "-" + d[4:6] + "-" + d[6:8] + " at " + d[9:11] + ":" + d[11:13] + ":" + d[13:15]

