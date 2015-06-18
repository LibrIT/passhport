# -*-coding:Utf-8 -*-

from app import db

"""Usergroup defines a group of users (can contain some usergroups too)"""
class Usergroup(db.Model):
    __tablename__ = "usergroup"
    id            = db.Column(db.Integer,     primary_key = True)
    usergroupname = db.Column(db.String(256), index = True, unique = True)
    comment       = db.Column(db.String(500), index = True, unique = False)

    # Relations
    members = db.relationship("Target", secondary = "target_group")

    def __repr__(self):
        """Return main data of the usergroup as a string"""
        output = []

        output.append("Usergroupname: {}".format(self.usergroupname.encode("utf8")))

        if self.comment:
            output.append("Comment: {}".format(self.comment.encode("utf8")))

        return "\n".join(output)

    def show_usergroupname(self):
        """Return a string containing the usergroup's name"""
        return self.usergroupname.encode("utf8")
