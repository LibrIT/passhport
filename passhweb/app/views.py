from flask import render_template, flash, redirect, session, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, mixins
from app import app, models, forms as f, requests_functions as rf, login_manager
from .models import User
from urllib.parse import urlparse, urljoin
from flask import request, url_for, stream_with_context, Response
import requests
import re
import config

### Utils ###
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def edit_form(element, form, name=None):
    """Return the form in a format acceptable for the post of this element"""
    if name:
        formated = {"name"        : name,
                    "new_name"    : form.name.data,
                    "new_comment" : form.comment.data+ " "}
    else:
        formated = {"name"    : form.name.data,
                    "comment" : form.comment.data}

    if element == "target":
        if name: 
            formated["new_hostname"]   = form.hostname.data
            formated["new_login"]      = form.login.data
            formated["new_port"]       = form.port.data
            formated["new_sshoptions"] = form.sshoptions.data + " "
            formated["new_targettype"] = form.targettype.data
            formated["new_changepwd"]  = form.changepwd.data
            formated["new_sessiondur"] = form.sessiondur.data
        else:
            formated["hostname"]   = form.hostname.data
            formated["login"]      = form.login.data
            formated["port"]       = form.port.data
            formated["sshoptions"] = form.sshoptions.data
            formated["targettype"] = form.targettype.data
            formated["changepwd"]  = form.changepwd.data
            formated["sessiondur"] = form.sessiondur.data
    elif element == "user":
        if name:
            formated["new_sshkey"] = form.sshkey.data
            # For log file size 3 possibilities : 0=unlimited,
            # any number=size in MB, Empty = Default
            if not form.logfilesize.data and  form.logfilesize.data != 0 :
                formated["new_logfilesize"] = "Default"
            else:
                formated["new_logfilesize"] = form.logfilesize.data
        else:
            formated["sshkey"] = form.sshkey.data
            if not form.logfilesize.data and form.logfilesize.data != 0 :
                formated["logfilesize"] = "Default"
            else:
                formated["logfilesize"] = form.logfilesize.data

    return formated


def is_manager(element=None, usergroupname=None):
    """ Return true if the user is manager and can handle the usergroup
    If nothing is passed in argument, we just check if he manages something"""
    if element == None:
        result = rf.get("user/ismanager/" + current_user.id)
        if result == "True":
            return True

    #Users can be managers of usergroups only
    elif element == "usergroup" :
        result = rf.get("usergroup/ismanager/" + usergroupname+ "/" + \
                        current_user.id)
        if result == "True":
            return True
    return False


def is_superadmin():
    """ Return true if the user is superadmin and can handle all objects """
    if config.LDAP == False:
        return True
    result = rf.get("user/issuperadmin/" + current_user.id)
    if result == "True":
        return True
    return False


def player():
    """ Return true if the user has access to a "jcd" player"""
    targetlist = rf.get("user/access/" + current_user.id)
    if targetlist:
        playerlist = [p for p in eval(targetlist) if p[:3] == "jcd"]
        if len(playerlist) > 0:
            return playerlist
    return False


def is_allowed(target):
    """ Return true if the user has access to this target """
    result = rf.get("user/accessible_target/" + \
                    current_user.id + "/" + target)
    if result == "True":
        return True
    else:
        return False


### Routes ###
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.errorhandler(500)
def internalError(error):
    try:
        userid = current_user.id
    except:
        userid = ""
    return render_template('pages/500.html',
                           pagename = "500",
                           userid = userid)


@app.errorhandler(404)
def pageNotFound(error):
    try:
        userid = current_user.id
    except:
        userid = ""
    return render_template('pages/404.html',
                           pagename = "404",
                           userid = userid)


@app.route('/logout')
@login_required
def logout():
    """Logout page (not a real page, it redirect immediatly)"""
    logout_user()
    return redirect('/login')


@app.route('/login',  methods=['GET', 'POST'])
def login():
    """Login page"""
    form = f.LoginForm()
    # POST :
    if form.validate_on_submit():
        if config.LOGINNOPWD == form.email.data:
            login_user(User(form.email.data))
        else:
            #Verify user/password through passhportd
            r = rf.post("user/login", {"login" : form.email.data,
                                       "password" : form.password.data})

            if r == "Authorized":
                login_user(User(form.email.data))
            else:
                login_manager.login_message = ""
                flash("Wrong credentials... try again!", "warning")
                return render_template('pages/login.html', 
                                        pagename = "Login",  
                                        form=form)

    else :
        # GET :
        if config.LDAP == True:
            return render_template('pages/login.html', 
                                   pagename = "Login",
                                   form=form)
        else:
            login_user(User("passhadmin"))

    # Next page
    next = request.args.get('next')
    app.logger.error(next)
    if not is_safe_url(next):
        return redirect(url_for('index'))
    return redirect(next or url_for('index'))




@app.route('/')
@app.route('/index')
@login_required
def index():
    # Index page contains: 
    # Welcome message
    # List of accessible databases with a button to ask access
    return render_template('pages/index.html', 
                            pagename = "Dashboard",
                            userid = current_user.id,
                            superadmin =  is_superadmin(),
                            managesomething = is_manager(),
                            player = player())


def writeonfile(data, filename):
    # Write text on a file, erasing the old one
    try:
        f = open(filename, "w")
        f.write(data)
        f.close()
    except:
        app.logger.error("Error writing " + filename + ". Contact support.")
        return False
    return True


@app.route('/config', methods=['GET', 'POST'])
@login_required
def genconfig():
    # Cofiguration generation,
    form = f.ConfigForm()

    if request.method == "POST":
        #Prepare different files
        writeonfile(request.form["pubsshkey"], config.PUBSSH)
        writeonfile(request.form["privsshkey"], config.PRIVSSH)
        writeonfile(request.form["sslkey"], config.SSLKEY)
        writeonfile(request.form["sslcert"], config.SSLCERT)
        app.logger.error(request.form)
        return redirect(url_for('index'))

    # GET
    if  config.LDAP == True :
        return  redirect(url_for('index'))

    return render_template('pages/firstconfig.html',
                            pagename = "Configuration",
                            userid = current_user.id,
                            superadmin = is_superadmin(),
                            form = form)


@app.route('/list/<element>')
@login_required
def listelement(element):
    """Return a listing page for the element type entered (target, user...)"""
    return render_template('pages/listelement.html', 
                           pagename = element + " list",
                           superadmin = is_superadmin(),
                           element = element,
                           userid = current_user.id,
                           managesomething = is_manager(),
                           player = player())


@app.route("/admin")
@login_required
def adminindex():
    """Return a page for administrator informations about paSShport"""
    if not is_superadmin():
        return redirect('/')

    return render_template('pages/superadmin.html',
                            pagename = "Administration",
                            superadmin = is_superadmin(),
                            DBP = config.DBP,
                            userid = current_user.id)


@app.route('/edit/<element>', defaults={'name': None}, methods=['GET', 'POST'])
@app.route('/edit/<element>/<name>', methods=['GET', 'POST'])
@login_required
def edit_element(element, name):
    """Return a page with element to create or edit an element"""
    # Form for the called element
    form = getattr(f, element.capitalize() + "Form")()
    # POST
    if request.method == "POST":
        # If we are on a specific name, it's an edition
        if name:
            print("Edition of " + element + ": " + name)
            r = rf.post(element + "/edit", edit_form(element, form, name))
        else:
            print("Creation of " + element +": " + form.name.data)
            r = rf.post(element + "/create", edit_form(element, form))

        if bool(re.search("^OK:", str(r))):
            # We need to reload the page if the name changed
            flash(form.name.data + " " + element +  " is saved", "success")
            if name != form.name.data:
                return redirect("/edit/" + element + "/" + form.name.data)
        else:
            flash("Error during edition process, please check the datas",
                   "danger")

    # GET - form presentation
    # Print the form with infos if a name is provided
    if name:
        if not is_superadmin() and not is_manager() and not is_allowed(name):
            return redirect('/')

        elt = rf.get_element(element, name)
        if element == "target":
            # Set target type for select2 field
            targettype = elt[0]["Target type"]
            form = f.TargetForm(targettype = targettype)
        return render_template('pages/' + element + '.html',
                               pagename = name,
                               userid = current_user.id, 
                               form = form,
                               me = name == current_user.id,
                               elt = elt,
                               superadmin =  is_superadmin(),
                               manager = is_manager(element, name),
                               managesomething = is_manager(),
                               is_allowed = is_allowed(name),
                               player = player(),
                               DBP = config.DBP)
    # Else print an empty form
    return render_template('pages/' + element + '.html',
                            pagename = element,
                            userid = current_user.id, 
                            superadmin =  is_superadmin(),
                            form = form,
                            player = player(),
                            DBP = config.DBP)


@app.route('/show/player/<name>', methods=['GET'])
@login_required
def show_player(name):
    """Return a page to download a file from a player #jcd"""
    #Check if the user can access this player
    if name not in player():
        return redirect('/')
    return render_template('pages/player.html',
                            pagename = name,
                            userid = current_user.id,
                            superadmin =  is_superadmin(),
                            managesomething = is_manager(),
                            is_allowed = is_allowed(name),
                            player = player())


@app.route('/download',  methods=['POST'])
@login_required
def indirectdownload():
    """Proxy the download from passhportd server"""
    target = request.form["targetname"]
    filename = request.form["filename"]
    data = {"filename" : filename,
             "target" : target}
    if 'player' in request.form:
        player = request.form["player"]
        data = {"filename" : filename,
                "target" : target,
                "player" : request.form["player"]}

    #First check user rights on this target
    if not is_allowed(target) or not filename:
        return render_template('pages/404.html',
                           pagename = "403",
                          userid = current_user.id)

    req = rf.proxypost("download", data = data)
    print("==> Retrive a file in streaming: " + target + ": " + filename)
    resp = Response(stream_with_context(req.iter_content(chunk_size=1024)), 
                    content_type = "application/octet-stream") 
    # Renaming the filename to be the same than the real
    resp.headers['Content-Disposition'] = "attachment; filename=" + \
                                          filename.split("/")[-1]
    return resp
    

#### AJAX ####
@app.route('/ajax/prepdownload', methods=['POST'])
@login_required
def aprepdownload():
    """Check if the file exist before launching a proper download"""
    target = request.form["targetname"]
    filename = request.form["filename"]   
    data = {"filename" : filename,
             "target" : target}
    if 'player' in request.form:
        player = request.form["player"]
        data = {"filename" : filename,
                "target" : target,
                "player" : request.form["player"]}

    #First check user rights on this target
    if not is_allowed(target) or not filename:
        return render_template('pages/404.html',
                               pagename = "403",
                               userid = current_user.id)
    
    req = rf.post("prepdownload", data = data)

    if req:
        if req == "OK":
            return "OK", 200, {"content-type": "text/plain; charset=utf-8"}
    return "KO", 404, {"content-type": "text/plain; charset=utf-8"}


@app.route('/ajax/list/<element>', defaults={'name': None})
@app.route('/ajax/list/<element>/<name>')
@login_required
def alistelement(element, name):
    if name and element != "player":
        elements = getattr(rf, "get_" + element +"_datatable")(name)
    elif element == "player":
        # need the username
        elements = getattr(rf, "get_" + element +"_datatable")(current_user.id)
    else:
        elements = getattr(rf, "get_" + element +"_datatable")()
    return elements


@app.route('/ajax/list/select2/<element>')
@login_required
def alistselect2element(element):
    """return a list of element in select2 format"""
    return getattr(rf, "get_" + element +"_select2")()


@app.route('/ajax/delete/<element>/<name>')
@login_required
def adelelement(element, name):
    """ Delete element from passhportd database... definitively"""
    if not is_superadmin():
        return "Not allowed", 403, \
               {"content-type": "text/plain; charset=utf-8"}
    result = rf.get(element + "/delete/" + name)
    return result


@app.route('/ajax/attached/<element>/<attached>/<eltname>')
@login_required
def aattachedelements(element, attached, eltname):
    """Return list of attached things(attached) from element (eltname)"""
    attachedelts = rf.get_attached_datatable(element, attached, eltname)
    return str(attachedelts)


@app.route('/ajax/addrm/<act>/<element>/<todel>', methods=["POST"])
@login_required
def rm_todel(act, element, todel):
    """Add or remove a "todel" (user/usergroup...) from element 
    (target, targetgroup...)"""
    # Only POST data are handled
    if request.method != "POST":
        return "Not allowed", 403, \
               {"content-type": "text/plain; charset=utf-8"}

    if not is_superadmin():
        if element == "usergroup":
            if not is_manager(element, request.form["usergroupname"]):
                return "Not allowed", 403, \
                       {"content-type": "text/plain; charset=utf-8"}
        else:
            return "Not allowed", 403, \
                   {"content-type": "text/plain; charset=utf-8"}

    return rf.addrmelt(element, todel, act, request.form, current_user.id)


@app.route('/ajax/access/<element>/<name>')
@login_required
def aaccesselement(element, name):
    """Return a list of all the targets accessible by this element"""
    targets = rf.get(element + "/access/" + name)
    return rf.listeltlink("target", targets)


@app.route('/ajax/memberof/<element>/<obj>/<name>')
@login_required
def amemberof(element, obj, name):
    """Return a list of obj the element is attached to"""
    objs = rf.get(element + "/memberof/" + obj + "/" + name)
    return rf.listeltlink(obj, objs)


@app.route('/ajax/target/lastconnections/<name>')
@login_required
def atargetlastconnections(name):
    """Return a datatable list of las logs dates and users for this target"""
    if is_superadmin() or  is_allowed(name):
        lastconnections = rf.get_target_lastconnections_datatable(name)
        return str(lastconnections)
    return "Not allowed", 403, \
               {"content-type": "text/plain; charset=utf-8"}


@app.route('/ajax/connection/ssh/current')
@login_required
def acurrentsshconnections():
    """Return a datable list of current SSH connections"""
    if not is_superadmin():
        return "Not allowed", 403, \
               {"content-type": "text/plain; charset=utf-8"}
    return str(rf.get_current_ssh_connections())


@app.route('/ajax/connection/db/current')
@login_required
def acurrentdbconnections():
    """Return a datable list of current databases connections"""
    if not is_superadmin():
        return "Not allowed", 403, \
               {"content-type": "text/plain; charset=utf-8"}
    return str(rf.get_current_db_connections())


@app.route('/ajax/connection/ssh/disconnect/<pid>')
@login_required
def asshdiconnection(pid):
    """Kill the PID on passhportd"""
    if not is_superadmin():
        return "Not allowed", 403, \
               {"content-type": "text/plain; charset=utf-8"}
    return rf.get("connection/ssh/disconnect/" + pid)


@app.route('/ajax/user/database/list')
@login_required
def aaccessible_database_list():
    """List the databases accessible by the user"""
    return rf.get_accessible_database_datatable(current_user.id)


@app.route('/ajax/user/database/access/<targetname>')
@login_required
def aaskaccess(targetname):
    """Ask passhportd to open a connection for this IP"""
    # IP can be hidden by proxy... except if it propagate it
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    
    return rf.get("exttargetaccess/open/" + ip + \
                  "/" + targetname + \
                  "/" + current_user.id)


@app.route('/ajax/user/database/access/close/<targetname>')
@app.route('/ajax/user/database/access/close/<targetname>/<username>')
@login_required
def acloseaccess(targetname, username = None):
    """Ask passhportd to close a connection (between user/target)"""
    if is_superadmin() and username != None:
        app.logger.error(targetname)
        app.logger.error(username)
        return rf.get("exttargetaccess/closebyname/" + targetname + "/" + username)
    return rf.get("exttargetaccess/closebyname/" + targetname + \
                  "/" + current_user.id)


@app.route('/ajax/target/password/<targetname>')
@login_required
def agetpassword(targetname):
    """List the last known root passwords of a target"""
    if is_superadmin() or is_allowed(targetname):
        return rf.get_password_datatable(targetname)
    return "Not allowed", 403, \
               {"content-type": "text/plain; charset=utf-8"}


@app.route('/ajax/namelist/<element>')
@login_required
def anamelist(element):
    """List all the elements of this kind"""
    names = rf.get_names_dict(element)
    if not names:
        return "[]"
    names = eval(names)
    # Format in json
    ret ="["
    for name in names:
        ret = ret + '{"value" : "' + name + '"},'
    ret = ret[:-1] + "]"
    return ret



