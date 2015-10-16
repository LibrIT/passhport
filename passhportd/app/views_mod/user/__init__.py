# -*- coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals
from io import open

import os
import config

from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import user, target


@app.route("/user/list")
def user_list():
    """Return the user list of database"""
    result = []
    query = db.session.query(user.User.name).order_by(user.User.name).all()

    for row in query:
        result.append(row[0])

    if not result:
        return "No user in database.", 200, \
            {"content-type": "text/plain; charset=utf-8"}

    return "\n".join(result), 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/user/search/<pattern>")
def user_search(pattern):
    """Return a list of users that match the given pattern"""
    result = []
    query  = db.session.query(user.User.name)\
        .filter(user.User.name.like("%" + pattern + "%"))\
        .order_by(user.User.name).all()

    for row in query:
        result.append(row[0])

    if not result:
        return 'No user matching the pattern "' + pattern + \
            '" found.', 200, {"content-type": "text/plain; charset=utf-8"}

    return "\n".join(result), 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/user/show/<name>")
def user_show(name):
    """Return all data about a user"""
    # Check for required fields
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    user_data = user.User.query.filter_by(name=name).first()

    if user_data is None:
        return 'ERROR: No user with the name "' + name + \
            '" in the database.', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    return user_data.__repr__(), 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/user/accessible_targets/<name>")
def user_accessible_targets(name):
    """Return the list of targets that the user can access"""
    # Check for required fields
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    user_data = user.User.query.filter_by(name=name).first()

    if user_data is None:
        return 'ERROR: No user with the name "' + name + \
            '" in the database.', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    target_list = user_data.accessible_target_list()
    formatted_target_list = []

    for each_target in target_list:
        formatted_target_list.append(each_target.show_name() + " " + \
        each_target.show_hostname())

    return "\n".join(formatted_target_list), 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/user/create", methods=["POST"])
def user_create():
    """Add a user in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    name = request.form["name"]
    sshkey = request.form["sshkey"]
    comment = request.form["comment"]

    # Check for required fields
    if not name or not sshkey:
        return "ERROR: The name and SSH key are required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check unicity for name
    query = db.session.query(user.User.name)\
        .filter_by(name=name).first()

    if query is not None:
        return 'ERROR: The name "' + name + \
            '" is already used by another user ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check unicity for SSH key
    query = db.session.query(user.User.sshkey)\
        .filter_by(sshkey=sshkey).first()

    if query is not None:
        return 'ERROR: The SSH key "' + sshkey + \
            '" is already used by another user ', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Add the SSH key in the file authorized_keys
    try:
        with open(config.SSH_KEY_FILE, "a", encoding="utf8") as \
            authorized_keys_file:
            authorized_keys_file.write('command=python"' + config.PASSHPORT_PATH + \
            " " + name + '" ' + sshkey + "\n")
    except IOError:
        return 'ERROR: cannot write in the file "authorized_keys"', 500, \
            {"content-type": "text/plain; charset=utf-8"}

    u = user.User(
        name=name,
        sshkey=sshkey,
        comment=comment)
    db.session.add(u)

    # Try to add the user on the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + name + '" -> ' + e.message , 409, \
            {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + name + '" -> created', 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/user/edit", methods=["POST"])
def user_edit():
    """Edit a user in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, \
            {"content-type": "text/plain; charset=utf-8"}

    # Simplification for the reading
    name = request.form["name"]
    new_name = request.form["new_name"]
    new_sshkey = request.form["new_sshkey"]
    new_comment = request.form["new_comment"]

    # Check required fields
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check if the name exists in the database
    query_check = db.session.query(user.User).filter_by(
        name=name).first()

    if query_check is None:
        return 'ERROR: No user with the name "' + name + \
            '" in the database.', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    to_update = db.session.query(user.User.name).filter_by(name=name)

    # Let's modify only relevent fields
    # Strangely the order is important, have to investigate why
    if new_comment:
        to_update.update({"comment": new_comment})

    if new_sshkey:
        # Check unicity for SSH key
        query = db.session.query(user.User)\
            .filter_by(sshkey=new_sshkey).first()

        if query is not None and query != query_check:
            return 'ERROR: The SSH key "' + new_sshkey + \
                '" is already used by another user ', 417, \
                {"content-type": "text/plain; charset=utf-8"}

        if new_sshkey != query_check.sshkey:
            # Edit the SSH key in the file authorized_keys
            try:
                with open(config.SSH_KEY_FILE, "r+", encoding="utf8") as \
                    authorized_keys_file:
                    line_edited = False
                    content = authorized_keys_file.readlines()
                    authorized_keys_file.seek(0)

                    for line in content:
                        if not line_edited:
                            if line != ('command=python"' + config.PASSHPORT_PATH + \
                            " " + name + '" ' + query_check.sshkey + "\n"):
                                authorized_keys_file.write(line)
                            else:
                                authorized_keys_file.write(
                                config.PASSHPORT_PATH + \
                                " " + new_name + '" ' + new_sshkey + "\n")
                                line_edited = True
                        else:
                            if line == ('command=python"' + config.PASSHPORT_PATH + \
                            " " + name + '" ' + query_check.sshkey + "\n"):
                                warning = ("WARNING: There is more " + \
                                "than one line with the sshkey " + \
                                query_check.sshkey + \
                                ", probably added manually. " + \
                                "You should edit it manually")

                            authorized_keys_file.write(line)

                    authorized_keys_file.truncate()
            except IOError:
                return 'ERROR: cannot write in the file "authorized_keys"', \
                500, {"content-type": "text/plain; charset=utf-8"}

        to_update.update({"sshkey": new_sshkey})

    if new_name:
        # Check unicity for name
        query = db.session.query(user.User)\
            .filter_by(name=new_name).first()

        if query != query_check and query is not None:
            return 'ERROR: The name "' + new_name + \
                '" is already used by another user ', 417, \
                {"content-type": "text/plain; charset=utf-8"}

        to_update.update({"name": new_name})

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + name + '" -> ' + e.message, 409, \
            {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + name + '" -> edited', 200, \
        {"content-type": "text/plain; charset=utf-8"}


@app.route("/user/delete/<name>")
def user_delete(name):
    """Delete a user in the database"""
    if not name:
        return "ERROR: The name is required ", 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Check if the name exists
    query = db.session.query(user.User).filter_by(name=name).first()

    if query is None:
        return 'ERROR: No user with the name "' + name + \
            '" in the database.', 417, \
            {"content-type": "text/plain; charset=utf-8"}

    # Delete the SSH key from the file authorized_keys
    warning = ""
    try:
        with open(config.SSH_KEY_FILE, "r+", encoding="utf8") as \
            authorized_keys_file:
            line_deleted = False
            content = authorized_keys_file.readlines()
            authorized_keys_file.seek(0)

            for line in content:
                if not line_deleted:
                    if line != ('command=python"' + config.PASSHPORT_PATH + \
                    " " + name + '" ' + query.sshkey + "\n"):
                        authorized_keys_file.write(line)
                    else:
                        line_deleted = True
                else:
                    if line == ('command=python"' + config.PASSHPORT_PATH + \
                    " " + name + '" ' + query.sshkey + "\n"):
                        warning = ("\nWARNING: There is more than one line "
                            "with the sshkey " + query.sshkey + ", probably "
                            "added manually. You should delete it manually")

                    authorized_keys_file.write(line)

            authorized_keys_file.truncate()
    except IOError:
        return 'ERROR: cannot write in the file "authorized_keys"', 500, \
            {"content-type": "text/plain; charset=utf-8"}

    db.session.query(
        user.User).filter(
        user.User.name == name).delete()

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + name + '" -> ' + e.message, 409, \
            {"content-type": "text/plain; charset=utf-8"}

    return 'OK: "' + name + '" -> deleted' + warning, 200, \
        {"content-type": "text/plain; charset=utf-8"}
