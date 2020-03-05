# -*-coding:Utf-8 -*-

import config
import os
import stat
import smtplib

from io import open
from sshpubkeys import SSHKey

from app import app, db
from app.models_mod import user
from app.models_mod import target
from app.models_mod import usergroup
from app.models_mod import targetgroup


"""Get the object which has the given name"""


def get_user(name):
    """Return the user with the given name"""
    u = db.session.query(user.User).filter(
        user.User.name == name).all()

    # User must exist in database
    if u:
        return u[0]
    else:
        return False


def get_target(name):
    """Return the target with the given name"""
    t = db.session.query(target.Target).filter(
        target.Target.name == name).all()

    # Target must exist in database
    if t:
        return t[0]
    else:
        return False


def get_usergroup(name):
    """Return the usergroup with the given usergroupname"""
    ug = db.session.query(usergroup.Usergroup).filter(
        usergroup.Usergroup.name == name).all()

    # Usergroup must exist in database
    if ug:
        return ug[0]
    else:
        return False


def get_targetgroup(name):
    """Return the targetgroup with the given name"""
    tg = db.session.query(targetgroup.Targetgroup).filter(
        targetgroup.Targetgroup.name == name).all()

    # Targetgroup must exist in database
    if tg:
        return tg[0]
    else:
        return False


def get_key(keyhash):
    """Return the user with this key or None if there is not"""
    # We are working with SHA256 hash for performances reason
    return db.session.query(user.User).filter(
            user.User.sshkeyhash.contains(keyhash)).first()


def response(errormsg, errorcode):
    """Return a HTTP formated response"""
    return errormsg, errorcode, {"content-type": "text/plain; charset=utf-8"}


def is_post(request):
    """Return False if the request is not a POST"""
    if request.method != "POST":
       return False
    return True


def check_user_get(request, name):
    """Do the checks and return a user object from the name"""
    # Only GET data are handled
    if request.method != "GET":
        return False

    # Check for required fields
    if not name:
        return False

    # Check if the name exists in the database
    query = db.session.query(user.User).filter_by(
        name=name).first()

    return query


def check_usergroup_get(request, name):
    """Do the checks and return a usergroup object from the name"""
    # Only GET data are handled
    if request.method != "GET":
        return False

    # Check for required fields
    if not name:
        return False

    # Check if the name exists in the database
    query = db.session.query(usergroup.Usergroup).filter_by(
        name=name).first()

    return query


def miss_mandatory(mandatory, form):
    """Return True if form miss mandatory fields"""
    for element in mandatory:
        if not form[element]:
            return True
    return False


def name_already_taken(name):
    """Return True if the name exist in database"""
    if get_user(name):
        return True
    return False


def sshkey_good_format(key):
    """Return False if the key hasn't a known format, else return a hash""" 
    sshkey = SSHKey(key, strict = True)

    try:
        sshkey.parse()
    except: 
        return False
    # We remove the "SHA256:" header and we add "=" at the end
    return sshkey.hash_sha256()[7:] + "="


def sshkey_already_taken(keyhash):
    """Return True if the ssh key hash already exist in database"""
    if get_key(keyhash):
        return True
    return False


def write_authorized_keys(name, sshkey):
    """Add the SSH key in authorize_keys with passhport call"""
    try:
        with open(config.SSH_KEY_FILE, "a", encoding="utf8") as \
                  authorized_keys_file:
                  authorized_keys_file.write('command="' + \
                                             config.PYTHON_PATH + \
                                             " " + config.PASSHPORT_PATH + \
                                             " " + name + '" ' + sshkey + "\n")
    except IOError:
        return response('ERROR: cannot write in the file ' + \
                        '"authorized_keys". However, the user is ' + \
                        'stored in the database.', 500)
    
    # set correct read/write permissions
    os.chmod(config.SSH_KEY_FILE, stat.S_IRUSR | stat.S_IWUSR)
    return True


def db_commit():
    """Commit on database"""
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return response('ERROR during database writing: -> ' + e.message , 409)
    return True 


def db_add_commit(elt):
    """Add an element to database and commit"""
    db.session.add(elt)
    return db_commit()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Notifications
def send_email(msg, subject, recipient):
    """Simply send the email to recipient"""
    server = smtplib.SMTP(config.NOTIF_SMTP)
    from_mail = config.NOTIF_FROM
    app.logger.info("Notification sent to: " + recipient)
    server.sendmail(from_mail, recipient, "Subject: " + subject + "\n\n" +msg)
    server.quit()


def notif(msg,subject="PaSSHport Notification", emergency="log"):
    """Send the msg via parmeters notification"""
    if emergency == "log":
            if config.NOTIF_LOG_TYPE == "email":
                for recipient in config.NOTIF_TO.split(","):
                    try:
                        send_email(msg, subject, recipient)
                    except:
                        app.logger.error("Error sending email. Check config.")
