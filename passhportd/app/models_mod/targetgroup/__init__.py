# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import db

# Table to handle the self-referencing many-to-many relationship
# for the Targetgroup class:
# First column holds the containers, the second the subgroups.
tgroup_of_tgroup = db.Table(
    "tgroup_of_tgroup",
    db.Column(
        "container_id",
        db.Integer,
        db.ForeignKey("targetgroup.id"),
        primary_key=True),
    db.Column(
        "subtargetgroup_id",
        db.Integer,
        db.ForeignKey("targetgroup.id"),
        primary_key=True))


class Targetgroup(db.Model):
    """Targetgroup defines a group of targets
    (can contain some targetgroups too)
    """
    __tablename__ = "targetgroup"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, unique=True)
    comment = db.Column(db.String(500), index=True, unique=False)

    # Relations
    members = db.relationship("User", secondary="tgroup_user")
    tmembers = db.relationship("Target", secondary="tgroup_target")
    gmembers = db.relationship("Usergroup", secondary="tgroup_group")
    tgmembers = db.relationship(
        "Targetgroup",
        secondary=tgroup_of_tgroup,
        primaryjoin=id == tgroup_of_tgroup.c.container_id,
        secondaryjoin=id == tgroup_of_tgroup.c.subtargetgroup_id,
        backref="containedin")

    def __repr__(self):
        """Return main data of the targetgroup as a string"""
        output = []

        output.append("Name: {}".format(self.name))
        output.append("Comment: {}".format(self.comment))
        output.append("User list:")

        for user in self.members:
            output.append(user.show_name())

        output.append("Target list:")

        for target in self.tmembers:
            output.append(target.show_name())

        output.append("Usergroup list:")

        for usergroup in self.gmembers:
            output.append(usergroup.show_name())

        output.append("Targetgroup list:")

        for targetgroup in self.tgmembers:
            output.append(targetgroup.show_name())

        output.append("All users: " + " ".join(self.all_user_list()))
        output.append("All targets: " + " ".join(self.all_target_list()))
        output.append("All usergroups: " + " ".join(self.all_usergroup_list()))
        output.append("All targetgroups: " + " ".join(self.all_targetgroup_list()))
        
        return "\n".join(output)

    def show_name(self):
        """Return a string containing the targetgroup’s name"""
        return self.name

    # User management
    def is_members(self, user):
        """Return true if the given user is a member
        of the targetgroup, false otherwise
        """
        return user in self.members

    def adduser(self, user):
        """Add a user to the relaton table"""
        if not self.is_members(user):
            self.members.append(user)

        return self

    def rmuser(self, user):
        """Remove a user from the relation table"""
        if self.is_members(user):
            self.members.remove(user)

        return self

    def username_in_targetgroup(self, username):
        """Return true if the given username belongs to a member
        of the targetgroup
        """
        for user in self.members:
            if user.show_name() == username:
                return True

        return False

    # Target management
    def is_tmembers(self, target):
        """Return true if the given target is a member
        of the targetgroup, false otherwise
        """
        return target in self.tmembers

    def addtarget(self, target):
        """Add a target to the relation table"""
        if not self.is_tmembers(target):
            self.tmembers.append(target)

        return self

    def rmtarget(self, target):
        """Remove a target from the relation table"""
        if self.is_tmembers(target):
            self.tmembers.remove(target)

        return self

    def targetname_in_targetgroup(self, targetname):
        """Return true if the given targetname belongs to a member
        of the targetgroup
        """
        for target in self.tmembers:
            if target.show_name() == targetname:
                return True

        return False

    # Usergroup management
    def is_gmembers(self, usergroup):
        """Return true if the given usergroup is a member
        of the targetgroup, false otherwise
        """
        return usergroup in self.gmembers

    def addusergroup(self, usergroup):
        """Add a usergroup to the relaton table"""
        if not self.is_gmembers(usergroup):
            self.gmembers.append(usergroup)

        return self

    def rmusergroup(self, usergroup):
        """Remove a usergroup from the relation table"""
        if self.is_gmembers(usergroup):
            self.gmembers.remove(usergroup)

        return self

    def usergroupname_in_targetgroup(self, usergroupname):
        """Return true if the given usergroupname belongs to a member
        of the targetgroup
        """
        for usergroup in self.gmembers:
            if usergroup.show_name() == usergroupname:
                return True

        return False

    # Targetgroup anagement
    def is_tgmembers(self, targetgroup):
        """Return true if the given targetgroup is a member
        of the targetgroup, false otherwise
        """
        return targetgroup in self.tgmembers

    def addtargetgroup(self, targetgroup):
        """Add a targetgroup to the relaton table"""
        if not self.is_tgmembers(targetgroup):
            self.tgmembers.append(targetgroup)

        return self

    def rmtargetgroup(self, targetgroup):
        """Remove a targetgroup from the relaton table"""
        if self.is_tgmembers(targetgroup):
            self.tgmembers.remove(targetgroup)

        return self

    def subtargetgroupname_in_targetgroup(self, subtargetgroupname):
        """Return true if the given subtargetgroupname belongs to a member
        of the targetgroup, false otherwise
        """
        for subtargetgroup in self.tgmembers:
            if subtargetgroup.show_name() == subtargetgroupname:
                return True

        return False

    def targetgroup_list(self):
        """Return targetgroups directly linked with the targetgroup"""
        targetgroups = []
        for targetgroup in self.tgmembers:
            targetgroups.append(targetgroup.show_name())

        return targetgroups

    def all_targetgroup_list(self, parsed_targetgroups = []):
        """Return a list with all the targetgroups of this targetgroup"""
        targetgroups = self.targetgroup_list()
        for targetgroup in self.tgmembers:
            if targetgroup not in parsed_targetgroups:
                parsed_targetgroups.append(targetgroup)
                for subtargetgroup in targetgroup.all_targetgroup_list(parsed_targetgroups):
                    if subtargetgroup not in targetgroups:
                        targetgroups.append(subtargetgroup)

        return targetgroups

    def usergroup_list(self):
        """Return usergroups directly linked with the targetgroup"""
        usergroups = []
        for usergroup in self.gmembers:
            usergroups.append(usergroup.show_name())

        return usergroups


    def all_usergroup_list(self, parsed_usergroups = []):
        """Return a list with all the usergroups of this targetgroup"""
        usergroups = self.usergroup_list()

        for usergroup in self.gmembers:
            if usergroup not in parsed_usergroups:
                parsed_usergroups.append(usergroup)
                for subusergroup in usergroup.all_usergroup_list(parsed_usergroups):
                    if subusergroup not in usergroups:
                        usergroups.append(subusergroup)

        return usergroups


    def target_list(self):
        """Return targets directly linked with the targetgroup"""
        targets = []
        for target in self.tmembers:
            targets.append(target.show_name())

        return targets


    def all_target_list(self, parsed_targetgroups = []):
        """Return a list with all the targets of this targetgroup"""
        targets = self.target_list()

        for targetgroup in self.tgmembers:
            if targetgroup not in parsed_targetgroups:
                parsed_targetgroups.append(targetgroup)
                for subtarget in targetgroup.all_target_list(parsed_targetgroups):
                    if subtarget not in targets:
                        targets.append(subtarget)

        return targets

    
    def user_list(self):
        """Return direct users"""
        users = []
        for user in self.members:
            users.append(user.show_name())

        return users


    def all_user_list(self, parsed_usergroups = []):
        """Return all users allowed to access the targetgroup"""
        users = self.user_list()

        # The only users allowed are those on usergroups. Not in targets or 
        # targetgroups
        for usergroup in self.gmembers:
            if usergroup not in parsed_usergroups:
                parsed_usergroups.append(usergroup)
                for user in usergroup.all_user_list(parsed_usergroups):
                    if user not in users:
                        users.append(user)

        return users

