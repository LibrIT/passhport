# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import db

# Table to handle the self-referencing many-to-many relationship for the Targetgroup class:
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

"""Targetgroup defines a group of targets (can contain some targetgroups too)"""


class Targetgroup(db.Model):
    __tablename__ = "targetgroup"
    id = db.Column(db.Integer, primary_key=True)
    targetgroupname = db.Column(db.String(256), index=True, unique=True)
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

        output.append(
            "Targetgroupname: {}".format(
                self.targetgroupname.encode('utf8')))
        output.append("Comment: {}".format(self.comment.encode('utf8')))
        output.append("User list:")

        for user in self.members:
            output.append(user.show_name())

        output.append("Target list:")

        for target in self.tmembers:
            output.append(target.show_name())

        output.append("Usergroup list:")

        for usergroup in self.gmembers:
            output.append(usergroup.show_usergroupname())

        output.append("Targetgroup list:")

        for targetgroup in self.tgmembers:
            output.append(targetgroup.show_targetgroupname())

        return "\n".join(output)

    def show_targetgroupname(self):
        """Return a string containing the targetgroup’s name"""
        return self.targetgroupname.encode("utf8")

    # Target management
    def is_tmembers(self, target):
        """Return true if the given target is a member of the targetgroup, false otherwise"""
        return target in self.tmembers

    def name_in_targetgroup(self, targetname):
        """Return true if the given targetname belongs to a member of the targetgroup"""
        for target in self.tmembers:
            if target.show_name() == targetname:
                return True

        return False

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

    # User management
    def is_members(self, user):
        """Return true if the given user is a member of the targetgroup, false otherwise"""
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

    # Usergroup management
    def is_gmembers(self, usergroup):
        """Return true if the given usergroup is a member of the targetgroup, false otherwise"""
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

    # Targetgroup anagement
    def is_tgmembers(self, targetgroup):
        """Return true if the given targetgroup is a member of the targetgroup, false otherwise"""
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
