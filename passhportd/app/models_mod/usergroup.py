# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import db, models_mod
from app.models_mod import target,targetgroup


# Table to handle the self-referencing many-to-many relationship
# for the Usergroup class:
# First column holds the containers, the second the subusergroups.
group_of_group = db.Table(
    "group_of_group",
    db.Column(
        "container_id",
        db.Integer,
        db.ForeignKey("usergroup.id"),
        primary_key=True),
    db.Column(
        "subgroup_id",
        db.Integer,
        db.ForeignKey("usergroup.id"),
        primary_key=True))


class Usergroup(db.Model):
    """Usergroup defines a group of users
    (can contain some usergroups too)
    """
    __tablename__ = "usergroup"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, unique=True)
    comment = db.Column(db.String(500), index=True, unique=False)

    # Relations
    members = db.relationship("User", secondary="group_user")
    targets = db.relationship("Target", secondary="target_group")
    tgmembers = db.relationship("Targetgroup", secondary="tgroup_group")
    gmembers = db.relationship(
        "Usergroup",
        secondary=group_of_group,
        primaryjoin=id == group_of_group.c.container_id,
        secondaryjoin=id == group_of_group.c.subgroup_id,
        backref="containedin")
    # Admins
    ugadmins = db.relationship("User", secondary="ug_admins")

    def __repr__(self):
        """Return main data of the usergroup as a string"""
        output = []

        output.append("Name: {}".format(self.name))
        output.append("Comment: {}".format(self.comment))
        output.append("User list: " + " ".join(self.username_list()))
        output.append("Usergroup list: " + " ".join(self.usergroupname_list()))

        output.append("All users: " + " ".join(self.all_username_list()))
        output.append("All usergroups: " + \
            " ".join(self.all_usergroupname_list()))

        return "\n".join(output)


    def simplejson(self):
        """Return a simplified data of the usergroup as json but not all the data"""
        directsize = len(self.members)
        totalsize = len(self.all_username_list())
        output = "{\n"
        output = output + "\"Name\": \"" + format(self.name) + "\",\n"
        output = output + "\"Comment\": \"" + format(self.comment) + "\",\n"
        output = output + "\"Directsize\": \"" + format(str(directsize)) + "\",\n"
        output = output + "\"Totalsize\": \"" + format(str(totalsize)) + "\"\n"
        output = output + "}"

        return output


    def show_name(self):
        """Return a string containing the usergroup's name"""
        return self.name


    def show_comment(self):
        """Return a string containing the usergroup's comment"""
        return self.comment


    # User management
    def is_member(self, user):
        """Return true if the given user is a member of the usergroup,
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


    def is_manager(self, user):
        """Return true if the given user is a manager of the usergroup,
        false otherwise
        """
        return user in self.ugadmins

    def name_is_manager(self, user):
        """Return true if the given username is manager"""
        for manager in self.ugadmins:
            if user == manager.name:
                return True
        return False


    def addmanager(self, user):
        """Add a manager to the relation table"""
        if not self.is_manager(user):
            self.ugadmins.append(user)

        return self


    def rmmanager(self, user):
        """Remove a maanger from the relation table"""
        if self.is_manager(user):
            self.ugadmins.remove(user)

        return self


    def rmtarget(self, target):
        """Remove a target from the relation table"""
        self.tmembers.remove(target)


    def rmtargetgroup(self, targetgroup):
        """Remove a group from the relation table"""
        self.tgmembers.remove(targetgroup)


    def username_in_usergroup(self, username):
        """Return true if the given username belongs to a member
        of the usergroup
        """
        for user in self.members:
            if user.show_name() == username:
                return True

        return False


    def manager_in_usergroup(self, username):
        """Return true if the given username belongs to a manager
        of the usergroup
        """
        for user in self.ugadmins:
            if user.show_name() == username:
                return True

        return False


    def username_list(self):
        """Return usernames which belong to users in the usergroup"""
        usernames = []

        for user in self.members:
            usernames.append(user.show_name())

        return usernames


    def all_username_list(self, parsed_usergroups = []):
        """Return all usernames which belong to users
        in the usergroup and subusergroups
        """
        usernames = self.username_list()

        # Recursive on groups:
        # we list all usernames but we never parse a group twice
        # to avoid cirular issues.
        for usergroup in self.gmembers:
            if usergroup not in parsed_usergroups:
                parsed_usergroups.append(usergroup)

                for username in usergroup.all_username_list(parsed_usergroups):
                    if username not in usernames:
                        usernames.append(username)

        return usernames


    def memberof(self, obj):
        """Return a string list of direct memberships of this usergroup"""
        if obj == "target":
            members = self.targets
        elif obj == "targetgroup":
            members = self.tgmembers
        elif obj == "usergroup":
            members = []
            query = db.session.query(models_mod.usergroup.Usergroup).all()
            for usergroup in query:
                if self in usergroup.gmembers:
                    members.append(usergroup)
        else:
            return "Error in object type"

        ret = "["
        for m in members:
            ret = ret + m.name + ","
        return ret[:-1] + "]"


    # Usergroup management
    def is_gmember(self, usergroup):
        """Return true if the given usergroup is a member
        of the usergroup, false otherwise
        """
        return usergroup in self.gmembers


    def addusergroup(self, usergroup):
        """Add a usergroup to the relation table"""
        if not self.is_gmember(usergroup) and not self == usergroup:
            self.gmembers.append(usergroup)
        else:
            return False

        return self


    def rmusergroup(self, usergroup):
        """Remove a usergroup from the relation table"""
        if self.is_gmember(usergroup):
            self.gmembers.remove(usergroup)

        return self


    def subusergroupname_in_usergroup(self, subusergroupname):
        """Return true if the given subusergroupname belongs to a member
        of the usergroup, false otherwise
        """
        for subusergroup in self.gmembers:
            if subusergroup.show_name() == subusergroupname:
                return True

        return False


    def usergroupname_list(self):
        """Return usergroupnames which belong to subusergroups
        in the usergroup
        """
        usergroupnames = []

        for usergroup in self.gmembers:
            usergroupnames.append(usergroup.show_name())

        return usergroupnames


    def all_usergroupname_list(self, parsed_usergroups = []):
        """Return all usergroupnames which belong to subusergroups
        in the usergroup
        """
        usergroupnames = self.usergroupname_list() # ["G1","G2"]

        # Recursive on usergroups:
        # we list all usergroups but we never parse a group twice
        # to avoid cirular issues.
        for subusergroup in self.gmembers:
            if subusergroup not in parsed_usergroups:
                parsed_usergroups.append(subusergroup) # [G1,G2]

                for subsubusergroupname in subusergroup.all_usergroupname_list(parsed_usergroups):
                    if subsubusergroupname not in usergroupnames:
                        usergroupnames.append(subsubusergroupname)

        return usergroupnames

    #List infos
    def list_direct_targets(self):
        """Return all the targets with this group as a direct member"""
        targets = []

        query = db.session.query(
            target.Target).order_by(
            target.Target.name).all()

        for each_target in query:
            if self in each_target.usergroup_list():
                targets.append(each_target.name)

        return targets


    def list_direct_targetgroups(self):
        """Return all the targetgroups with this group as a direct member"""
        targetgroups = []

        query = db.session.query(
            targetgroup.Targetgroup).order_by(
            targetgroup.Targetgroup.name).all()

        for each_targetgroup in query:
            if self in each_targetgroup.usergroup_list():
                targetgroups.append(each_targetgroup)

        return targetgroups


    def list_direct_usergroups(self):
        """Return all the usergroups with this group as a direct member"""
        usergroups = []

        query = db.session.query(
            Usergroup).order_by(
            Usergroup.name).all()

        for each_usergroup in query:
            if self in each_usergroup.gmembers:
                usergroups.append(each_usergroup)

        return usergroups


    def accessible_target_list(self, checked_usergroups = [], mode="string"):
        """Return all the targets this usergroups give access to"""
        accessible_targets = []
        checked_usergroups.append(self)

        # 1. list all the directly attached targets
        for target in self.targets:
            if mode == "string":
                accessible_targets.append(target.name)
            else:
                accessible_targets.append(target)

        # 2. list all targets accessible through usergroups
        for usergroup in self.containedin:
            if usergroup not in checked_usergroups:
                checked_usergroups.append(usergroup)
                for target in usergroup.accessible_target_list(
                                         checked_usergroups, mode="obj"):
                    if target not in accessible_targets:
                        if mode == "string":
                            print(target)
                            accessible_targets.append(target.name)
                        else:
                            accessible_targets.append(target)

        # 3. list all the target accessible through targetgroups
        for targetgroup in self.tgmembers:
            for target in targetgroup.accessible_target_list():
                if target not in self.targets:
                    if mode == "string":
                        accessible_targets.append(target.name)
                    else:
                        accessible_targets.append(target)

        return accessible_targets


    def show_targets(self, indentation):
        """Return all targets the group gives access
        First the targets with this group attached
        Then targets from targetgroups with this group attached
        Then targets from groups with this group attached
        Finally We relaunch this on the groups with this groups attached
        """
        listing = []
        indent = ""
        for i in range(indentation):
            indent = indent + "    "

        #We add the group only if he contains targets else it hard to read
        direct_targets = self.list_direct_targets()
        if direct_targets:
            listing.append(indent + "Access via " + self.name + ": \n" + \
                indent + "    Targets: " + \
                " ".join(direct_targets) + "\n")

        #And for the groups
        direct_usergroups = self.list_direct_usergroups()
        if direct_usergroups:
            #Print the name of the usergroup followed by target allowed
            for each_usergroup in direct_usergroups:
                group_targets = each_usergroup.show_targets(indentation + 1)
                if group_targets:
                    listing.append(indent + "    " + self.name + \
                            " member of " + each_usergroup.name + "\n")
                    listing.append(indent + \
                            "\n".join(group_targets))

        #Same for targetgroups
        direct_targetgroups = self.list_direct_targetgroups()
        if direct_targetgroups:
            for each_targetgroup in direct_targetgroups:
                targetgroups = each_targetgroup.show_targets(indentation + 1)
                if targetgroups:
                    listing.append(indent + "    " + self.name + \
                            " member of " + each_targetgroup.name + "\n")
                    listing.append(indent + \
                            "\n".join(targetgroups))

        return listing


    def prepare_delete(self):
        """Remove all elements of this usergroup"""
        while len(self.members) > 0:
            self.members.pop()
        while len(self.gmembers) > 0:
            self.gmembers.pop()
        while len(self.ugadmins) > 0:
            self.ugadmins.pop()
        while len(self.targets) > 0:
            self.targets.pop()
        while len(self.tgmembers) > 0:
            self.tgmembers.pop()


### JSON ###
    def username_list_json(self):
        """Return all the direct users names"""
        usernames = ""

        for user in self.members:
            usernames = usernames + \
                        "{\"Name\" : \"" + user.show_name() + "\"," + \
                        "\"Comment\" : \"" + user.show_comment() + "\"},"

        return usernames[:-1]


    def managername_list_json(self):
        """Return all the direct managers names"""
        names = ""

        for user in self.ugadmins:
            names = names + "{\"Name\" : \"" + user.show_name() + "\"," + \
                    "\"Comment\" : \"" + user.show_comment() + "\"},"

        return names[:-1]


    def usergroupname_list_json(self):
        """Return all the direct usergoups names"""
        usergroupnames = ""

        for usergroup in self.gmembers:
            usergroupnames = usergroupnames + "{\"Name\" : \"" + \
                             usergroup.show_name() + "\"," + \
                             "\"Comment\" : \"" + \
                             usergroup.show_comment() + "\"},"

        return usergroupnames[:-1]
