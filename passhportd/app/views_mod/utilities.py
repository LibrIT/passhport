# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import app, db
from app.models_mod import user, target, usergroup, targetgroup


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

def response(errormsg, errorcode):
    """Return a HTTP formated response"""
    return errormsg, errorcode, {"content-type": "text/plain; charset=utf-8"}


