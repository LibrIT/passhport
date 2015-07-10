# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import db

"""User defines information for every adminsys using passhport"""


class User(db.Model):
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

        return "\n".join(output)

    def show_name(self):
        """Return a string containing the user's name"""
        return self.name.encode("utf8")
