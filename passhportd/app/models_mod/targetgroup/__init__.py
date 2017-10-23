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
    # Admins - can admin usergroups and targetgroups (add and remove users)
    tgadmins = db.relationship("User", secondary="tg_admins")

    def __repr__(self):
        """Return main data of the targetgroup as a string"""
        output = []

        output.append("Name: {}".format(self.name))
        output.append("Comment: {}".format(self.comment))
        output.append("User list: " + " ".join(self.username_list()))
        output.append("Target list: " + " ".join(self.targetname_list()))
        output.append("Usergroup list: " + " ".join(self.usergroupname_list()))
        output.append("Targetgroup list: " + " ".join(self.targetgroupname_list()))

        output.append("All users: " + " ".join(self.all_username_list()))
        output.append("All targets: " + " ".join(self.all_targetname_list()))
        output.append("All usergroups: " + " ".join(self.all_usergroupname_list()))
        output.append("All targetgroups: " + " ".join(self.all_targetgroupname_list()))

        return "\n".join(output)

    def simplejson(self):
        """Return a simplified data of the target as json but not all the data"""
        output = "{\n"

        output = output + "\"name\": \"" + format(self.name) + "\",\n"
        output = output + "\"comment\": \"" + format(self.comment) + "\",\n"
        output = output + "}"

        return output

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


    def username_list(self):
        """Return usernames which belong to users in the targetgroup"""
        usernames = []

        for user in self.members:
            usernames.append(user.show_name())

        return usernames


    def all_username_list(self, parsed_usergroups = None):
        """Return all users allowed to access the targetgroup"""
        if parsed_usergroups is None :
            parsed_usergroups = []

        usernames = self.username_list()

        # The only users allowed are those on usergroups. Not in targets or
        # targetgroups
        for usergroup in self.gmembers:
            if usergroup not in parsed_usergroups:
                parsed_usergroups.append(usergroup)

                for username in usergroup.all_username_list(parsed_usergroups):
                    if username not in usernames:
                        usernames.append(username)

        return usernames


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


    def targetname_list(self):
        """Return targets directly linked with the targetgroup"""
        targetnames = []

        for target in self.tmembers:
            targetnames.append(target.show_name())

        return targetnames


    def all_targetname_list(self, parsed_targetgroups = None):
        """Return a list with all the targets of this targetgroup"""
        if parsed_targetgroups is None :
            parsed_targetgroups = []

        targetnames = self.targetname_list()

        for targetgroup in self.tgmembers:
            if targetgroup not in parsed_targetgroups:
                parsed_targetgroups.append(targetgroup)

                for targetname in targetgroup.all_targetname_list(parsed_targetgroups):
                    if targetname not in targetnames:
                        targetnames.append(targetname)

        return targetnames


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


    def usergroupname_list(self):
        """Return names of usergroups directly linked with the targetgroup"""
        usergroupnames = []
        for usergroup in self.gmembers:
            usergroupnames.append(usergroup.show_name())

        return usergroupnames


    def usergroup_list(self):
        """Return usergroups directly linkked with the targetgroup"""
        usergroupnames = []
        for usergroup in self.gmembers:
            usergroupnames.append(usergroup)

        return usergroupnames


    def all_usergroupname_list(self, parsed_usergroups = None):
        """Return a list with all the usergroups of this targetgroup"""
        if parsed_usergroups is None:
            parsed_usergroups = []

        usergroupnames = self.usergroupname_list()

        for usergroup in self.gmembers:
            if usergroup not in parsed_usergroups:
                parsed_usergroups.append(usergroup)

                for usergroupname in usergroup.all_usergroupname_list(parsed_usergroups):
                    if usergroupname not in usergroupnames:
                        usergroupnames.append(usergroupname)

        return usergroupnames


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


    def targetgroupname_list(self):
        """Return targetgroups directly linked with the targetgroup"""
        targetgroupnames = []

        for targetgroup in self.tgmembers:
            targetgroupnames.append(targetgroup.show_name())

        return targetgroupnames


    def all_targetgroupname_list(self, parsed_targetgroups = None):
        """Return a list with all the targetgroups of this targetgroup"""
        if parsed_targetgroups is None:
            parsed_targetgroups = []

        targetgroupnames = self.targetgroupname_list()

        for subtargetgroup in self.tgmembers:
            if subtargetgroup not in parsed_targetgroups:
                parsed_targetgroups.append(subtargetgroup)

                for subtargetgroupname in subtargetgroup.all_targetgroupname_list(parsed_targetgroups):
                    if subtargetgroupname not in targetgroupnames:
                        targetgroupnames.append(subtargetgroupname)

        return targetgroupnames

    def show_targets(self, indentation):
        """Return a formated list of the targets that the targetgroup 
        provides
        """
        listing = []
        
        indent = ""
        for i in range(indentation):
            indent = indent + "    "

        #Adding direct targets
        if self.tmembers:
            toappend = indent + "Access via " + self.name + ": \n" + \
                    indent + "    Targets: "
            for target in self.tmembers:
                toappend = toappend + target.name  + "\n"
            listing.append(toappend)


        #Recusrsivity on targetgroups
        if self.tgmembers:
            for targetgroup in self.tgmembers:
                listing.append(targetgroup.show_targets(indentation + 1))

        return listing
