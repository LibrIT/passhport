# -*-coding:Utf-8 -*-

from app import db

"""Targetgroup defines a group of targets (can contain some targetgroups too)"""
class Targetgroup(db.Model):
    __tablename__   = "targetgroup"
    id              = db.Column(db.Integer,     primary_key = True)
    targetgroupname = db.Column(db.String(256), index = True, unique = True)
    comment         = db.Column(db.String(500), index = True, unique = False)

    # Relations
    members   = db.relationship("User",        secondary = "tgroup_user")
    tmembers  = db.relationship("Target",      secondary = "tgroup_target")
    gmembers  = db.relationship("Usergroup",   secondary = "tgroup_group")

    def __repr__(self):
        """Return main data of the targetgroup as a string"""
        output = []

        output.append("Targetgroupname: {}".format(self.targetgroupname.encode('utf8')))
        output.append("Comment: {}".format(self.comment.encode('utf8')))
        output.append("User list:")

        for user in self.members:
            output.append(user.show_email())

        output.append("Target list:")

        for target in self.tmembers:
            output.append(target.show_name())

        return "\n".join(output)

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
