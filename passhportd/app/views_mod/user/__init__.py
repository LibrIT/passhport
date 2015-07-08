# -*-coding:Utf-8 -*-

from flask import request
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from app import app, db
from app.models_mod import user


@app.route("/user/list")
def user_list():
    """Return the user list of database"""
    result = []
    query = db.session.query(user.User.email).order_by(user.User.email).all()

    for row in query:
        result.append(row[0].encode("utf8"))

    if not result:
        return "No user in database.\n", 200, {"Content-Type": "text/plain"}

    return "\n".join(result), 200, {"Content-Type": "text/plain"}


@app.route("/user/search/<pattern>")
def user_search(pattern):
    """Return a list of users that match the given pattern"""
    """
    To check
        Specific characters
        upper and lowercases
    """

    result = []
    query  = db.session.query(user.User.email)\
        .filter(user.User.email.like("%" + pattern + "%")).all()

    for row in query:
        result.append(row[0].encode("utf8"))

    if not result:
        return 'No user matching the pattern "' + pattern + \
            '" found.\n', 200, {"Content-Type": "text/plain"}

    return "\n".join(result), 200, {"Content-Type": "text/plain"}


@app.route("/user/show/<email>")
def user_show(email):
    """Return all data about a user"""
    """
    To check
        Specific characters
        upper and lowercases
    """

    # Check for required fields
    if not email:
        return "ERROR: The email is required ", 417, {
            "Content-Type": "text/plain"}

    user_data = user.User.query.filter_by(email=email).first()

    if user_data is None:
        return 'ERROR: No user with the email "' + email + \
            '" in the database.\n', 417, {"Content-Type": "text/plain"}

    return str(user_data), 200, {"Content-Type": "text/plain"}


@app.route("/user/create", methods=["POST"])
def user_create():
    """Add a user in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    email = request.form["email"]
    sshkey = request.form["sshkey"]
    comment = request.form["comment"]

    # Check for required fields
    if not email or not sshkey:
        return "ERROR: The email and SSH key are required ", 417, {
            "Content-Type": "text/plain"}

    # Check unicity for email
    query = db.session.query(user.User.email)\
        .filter_by(email=email).first()

    if query is not None:
        return 'ERROR: The email "' + email + \
            '" is already used by another user ',\
             417, {"Content-Type": "text/plain"}

    # Check unicity for SSH key
    query = db.session.query(user.User.sshkey)\
        .filter_by(sshkey=sshkey).first()

    if query is not None:
        return 'ERROR: The SSH key "' + sshkey + \
            '" is already used by another user ',\
             417, {"Content-Type": "text/plain"}

    u = user.User(
        email=email,
        sshkey=sshkey,
        comment=comment)
    db.session.add(u)

    # Try to add the user on the database
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + email + '" -> ' + e.message + \
            "\n", 409, {"Content-Type": "text/plain"}

    return 'OK: "' + email + '" -> created' + \
        "\n", 200, {"Content-Type": "text/plain"}


@app.route("/user/edit", methods=["POST"])
def user_edit():
    """Edit a user in the database"""
    # Only POST data are handled
    if request.method != "POST":
        return "ERROR: POST method is required ", 405, {
            "Content-Type": "text/plain"}

    # Simplification for the reading
    email = request.form["email"]
    new_email = request.form["new_email"]
    new_sshkey = request.form["new_sshkey"]
    new_comment = request.form["new_comment"]

    # Check required fields
    if not email:
        return "ERROR: The email is required ", 417, {
            "Content-Type": "text/plain"}

    # Check if the email exists in the database
    query = db.session.query(user.User).filter_by(email=email).first()

    if query is None:
        return 'ERROR: No user with the email "' + email + \
            '" in the database.\n', 417, {"Content-Type": "text/plain"}

    to_update = db.session.query(user.User).filter_by(email=email)

    # Let's modify only relevent fields
    # Strangely the order is important, have to investigate why
    if new_comment:
        to_update.update({"comment": new_comment.encode("utf8")})
    if new_sshkey:
        # Check unicity for SSH key
        query = db.session.query(user.User.sshkey)\
            .filter_by(sshkey=new_sshkey).first()

        if query is not None and new_sshkey != query.sshkey:
            return 'ERROR: The SSH key "' + new_sshkey + \
                '" is already used by another user ', \
                417, {"Content-Type": "text/plain"}

        to_update.update({"sshkey": new_sshkey.encode("utf8")})
    if new_email:
        # Check unicity for email
        query = db.session.query(user.User.email)\
            .filter_by(email=new_email).first()

        if query is not None and new_email != query.email:
            return 'ERROR: The email "' + new_email + \
                '" is already used by another user ', \
                417, {"Content-Type": "text/plain"}

        to_update.update({"email": new_email.encode("utf8")})

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + email + '" -> ' + e.message + \
            "\n", 409, {"Content-Type": "text/plain"}

    return 'OK: "' + email + '" -> edited' + \
        "\n", 200, {"Content-Type": "text/plain"}


@app.route("/user/delete/<email>")
def user_delete(email):
    """Delete a user in the database"""
    if not email:
        return "ERROR: The email is required ", 417, {
            "Content-Type": "text/plain"}

    # Check if the email exists
    query = db.session.query(user.User).filter_by(email=email).first()

    if query is None:
        return 'ERROR: No user with the email "' + email + \
            '" in the database.\n', 417, {"Content-Type": "text/plain"}

    db.session.query(
        user.User).filter(
        user.User.email == email).delete()

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        return 'ERROR: "' + email + '" -> ' + e.message + \
            "\n", 409, {"Content-Type": "text/plain"}

    return 'OK: "' + email + '" -> deleted' + \
        "\n", 200, {"Content-Type": "text/plain"}
