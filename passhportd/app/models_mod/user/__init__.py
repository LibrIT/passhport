# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import app, db
from app.models_mod import target


class User(db.Model):
    """User defines information for every adminsys using passhport"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    sshkey = db.Column(
        db.String(500),
        index=False,
        unique=True,
        nullable=False)
    comment = db.Column(db.String(500), index=True)

    # Relations
    targets = db.relationship("Target", secondary="target_user")


    def __repr__(self):
        """Return main data of the user as a string"""
        output = []

        output.append("Name: {}".format(self.name))
        output.append("SSH key: {}".format(self.sshkey))
        output.append("Comment: {}".format(self.comment))
        output.append("Accessible target list: " + \
            " ".join(self.accessible_targetname_list()))

        return "\n".join(output)


    def show_name(self):
        """Return a string containing the user's name"""
        return self.name


    def accessible_targetname_list(self):
        """Return target names which are accessible to the user"""
        targetnames = []

        query = db.session.query(
            target.Target).order_by(
            target.Target.name).all()

        for each_target in query:
            if self.name in each_target.list_all_usernames():
                targetnames.append(each_target.show_name())

        return targetnames

    def accessible_target_list(self):
        """Return target objects which are accessible to the user"""
        targets = []

        query = db.session.query(
            target.Target).order_by(
            target.Target.name).all()

        for each_target in query:
            if self.name in each_target.list_all_usernames():
                targets.append(each_target)

        return targets
