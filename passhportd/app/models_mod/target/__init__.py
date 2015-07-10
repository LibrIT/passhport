# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import db

"""Target defines information for every server accessible through passhport"""


class Target(db.Model):
    __tablename__ = "target"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, unique=True)
    hostname = db.Column(db.String(120), index=True, nullable=False)
    port = db.Column(db.Integer, index=False)
    sshoptions = db.Column(db.String(500), index=True)
    servertype = db.Column(db.String(64), index=True)
    autocommand = db.Column(db.String(128), index=True)
    comment = db.Column(db.String(500), index=True)

    # Relations
    members = db.relationship("User", secondary="target_user")
    gmembers = db.relationship("Usergroup", secondary="target_group")

    def __repr__(self):
        """Return main data of the target as a string"""
        output = []

        output.append("Name: {}".format(self.name))
        output.append("Hostname: {}".format(self.hostname))
        output.append("Port: {}".format(str(self.port)))
        output.append("SSH options: {}".format(self.sshoptions))
        output.append("Servertype: {}".format(self.servertype))
        output.append(
            "Autocommand: {}".format(
                self.autocommand))
        output.append("Comment: {}".format(self.comment))
        output.append("User list:")

        for user in self.members:
            output.append(user.show_name())

        output.append("Usergroup list:")

        for usergroup in self.gmembers:
            output.append(usergroup.show_usergroupname())

        return "\n".join(output)

    def show_name(self):
        """Return a string containing the target's name"""
        return self.name

    # User management
    def adduser(self, user):
        """Add a user to the relation table"""
        if not self.is_member(user):
            self.members.append(user)

        return self

    def rmuser(self, user):
        """Remove a user from the relation table"""
        if self.is_member(user):
            self.members.remove(user)

        return self

    def is_member(self, user):
        """Return true if the given user is a member of the target, false otherwise"""
        return user in self.members

    def name_in_target(self, name):
        """Return true if the given name belongs to a member of the target"""
        for user in self.members:
            if user.show_name() == name:
                return True

        return False

    # Usergroup management
    def addusergroup(self, usergroup):
        """Add a usergroup to the relation table"""
        if not self.is_gmember(usergroup):
            self.gmembers.append(usergroup)

        return self

    def rmusergroup(self, usergroup):
        """Remove a usergroup to the relation table"""
        if self.is_gmember(usergroup):
            self.gmembers.remove(usergroup)

        return self

    def is_gmember(self, usergroup):
        """Return true if the given usergroup is a member of the target, false otherwise"""
        return usergroup in self.gmembers

    def usergroupname_in_target(self, usergroupname):
        """Return true if the given usergroupname belongs to a member of the target"""
        for usergroup in self.gmembers:
            if usergroup.show_usergroupname() == usergroupname:
                return True

        return False
