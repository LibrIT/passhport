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
        output.append("User list: " + " ".join(self.user_list()))
        output.append("Usergroup list: " + " ".join(self.usergroup_list()))

        output.append("All users: " + " ".join(self.list_all_users()))
        output.append("All usergroups: " + " ".join(self.list_all_usergroups()))
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

    def user_list(self):
        """Return all the direct users from the target"""
        users = []
        for user in self.members:
            users.append(user.show_name())

        return users

    def user_object_list(self):
        """Return all the direct users from the target"""
        users = []
        for user in self.members:
            users.append(user)

        return users

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

    def usergroups_users(self):
        """Return all the users from the target usergroups"""
        Users = {}
        return USers

    def usergroup_list(self):
        """Return all the direct usergroups from the target"""
        usergroups = []
        for usergroup in self.gmembers:
            usergroups.append(usergroup.show_name())

        return usergroups
    
    def usergroup_object_list(self):
        """Return all the direct usergroups objects from the target"""
        usergroups = []
        for usergroup in self.gmembers:
            usergroups.append(usergroup)

        return usergroups
       
    # Access management
    def list_all_users(self):
        """Return a list with all the user who can access
        this target
        """
        users = self.user_list()
        for group in self.usergroup_object_list():
            for user in group.all_user_list():
                if user not in users:
                   users.append(user)

        return users

    def list_all_usergroups(self):
        """Return a list with all the usergroup who can access
        this target
        """
        usergroups = self.usergroup_list()
        for group in self.usergroup_object_list():
            for subgroup in group.all_usergroup_list():
                if subgroup not in usergroups:
                   usergroups.append(subgroup)

        return usergroups

