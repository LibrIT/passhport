# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import db


class Target(db.Model):
    """Target defines information for every server accessible
    through passhport
    """
    __tablename__ = "target"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, unique=True)
    hostname = db.Column(db.String(120), index=True, nullable=False)
    port = db.Column(db.Integer, index=False)
    sshoptions = db.Column(db.String(500), index=True)
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
        output.append("Comment: {}".format(self.comment))
        output.append("User list:")

        for user in self.members:
            output.append(user.show_name())

        output.append("Usergroup list:")

        for usergroup in self.gmembers:
            output.append(usergroup.show_name())

        return "\n".join(output)

    def show_name(self):
        """Return a string containing the target's name"""
        return self.name

    # User management
    def is_member(self, user):
        """Return true if the given user is a member of the target,
        false otherwise
        """
        return user in self.members

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

    def username_in_target(self, username):
        """Return true if the given username belongs to a member
        of the target
        """
        for user in self.members:
            if user.show_name() == username:
                return True

        return False

    # Usergroup management
    def is_gmember(self, usergroup):
        """Return true if the given usergroup is a member
        of the target, false otherwise
        """
        return usergroup in self.gmembers

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

    def usergroupname_in_target(self, usergroupname):
        """Return true if the given usergroupname belongs to a member
        of the target
        """
        for usergroup in self.gmembers:
            if usergroup.show_name() == usergroupname:
                return True

        return False
