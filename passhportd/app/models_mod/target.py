# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from datetime import datetime, timedelta, date
from app import app, db
from app.models_mod import targetgroup
from flask import jsonify


class Target(db.Model):
    """Target defines information for every server accessible
    through passhport
    """
    __tablename__ = "target"
    id = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(256), index=True, unique=True)
    hostname   = db.Column(db.String(120), index=True, nullable=False)
    targettype = db.Column(db.String(120), index=True, server_default="ssh")
    login      = db.Column(db.String(120), index=True)
    port       = db.Column(db.Integer, index=False)
    sshoptions = db.Column(db.String(500), index=True)
    comment    = db.Column(db.String(500), index=True)

    # Relations
    members    = db.relationship("User", secondary="target_user")
    gmembers   = db.relationship("Usergroup", secondary="target_group")
    memberoftg = db.relationship("Targetgroup", secondary="tgroup_target")
    logentries = db.relationship("Logentry", secondary="target_log")
    passentries = db.relationship("Passentry", secondary="target_pass")
    exttargetaccess = db.relationship("Exttargetaccess", 
                                      secondary="target_extaccess")


    def __repr__(self):
        """Return main data of the target as a string"""
        output = []
        output.append("Name: {}".format(self.name))
        output.append("Hostname: {}".format(self.hostname))
        output.append("Target type : {}".format(self.targettype))
        output.append("Login: {}".format(self.login))
        output.append("Port: {}".format(str(self.port)))
        output.append("SSH options: {}".format(self.sshoptions))
        output.append("Comment: {}".format(self.comment))
        output.append("Attached users: " + " ".join(self.username_list()))
        output.append("Usergroup list: " + " ".join(self.usergroupname_list()))

        output.append("Users who can access this target: " + " ".join(self.list_all_usernames()))
        output.append("All usergroups: " + " ".join(self.list_all_usergroupnames()))

        output.append("Member of the following targetgroups: " + " ".join(self.list_all_targetgroupnames()))

        return "\n".join(output)


    def simplejson(self):
        """Return a simplified data of the target as json but not all the data"""
        output = "{\n"

        output = output + "\"Name\": \"" + format(self.name) + "\",\n"
        output = output + "\"Hostname\": \"" + format(self.hostname) + "\",\n"
        output = output + "\"Target type\": \"" + format(self.show_targettype()) + "\",\n"
        output = output + "\"Login\": \"" + format(self.login) + "\",\n"
        output = output + "\"Port\": \"" + format(self.port) + "\",\n"
        output = output + "\"SSH options\": \"" + format(self.sshoptions) + "\",\n"
        output = output + "\"Comment\": \"" + format(self.comment) + "\"\n"
        output = output + "}"

        return output
        

    def show_name(self):
        """Return a string containing the target's name"""
        return self.name


    def show_hostname(self):
        """Return a string containing the target's hostname"""
        return self.hostname
    
    
    def show_login(self):
        """Return a string containing the targets login"""
        if not self.login:
            return "root"
        return self.login


    def show_port(self):
        """Return an int containing the target's port"""
        if not self.port:
            return 22
        return self.port

    def show_options(self):
        """Return a string with the options"""
        return self.sshoptions
    

    def show_targettype(self):
        """Return a string containing the target's targettype"""
        if not self.targettype:
            return "ssh"
        return self.targettype
    

    def show_comment(self):
        """Return a string containing the target's comment"""
        return self.comment


    def memberof(self, obj):
        """Return a string list of direct memberships of this target"""
        if obj == "targetgroup":
            members = self.memberoftg
        else:
            return "Error in object type"
            
        ret = "["
        for m in members:
            ret = ret + m.name + ","
        return ret[:-1] + "]"
    

    def prepare_delete(self):
        """Remove relationships before deletion"""
        while len(self.members) > 0:
            self.members.pop()
        while len(self.gmembers) > 0:
            self.gmembers.pop()
        # Remove the target from targetgroup is handled in the view
        while len(self.logentries) > 0:
            self.logentries.pop()


    # Pass management
    def addpassentry(self, passentry):
        """Add a reference on a password changed on this target"""
        self.passentries.append(passentry)
        return self
    

    # Log management
    def addlogentry(self, logentry):
        """Add a reference on a connexion made on this target"""
        self.logentries.append(logentry)
        return self
    

    def get_lastlog(self):
        """Return 500 last log entries as json"""
        output = "{\n"
        if len(self.logentries) < 1:
            return "{}"

        for i in range(0, 500):
            if i >= len(self.logentries):
                i = 500
            else:
                output = output + '"' + str(i) + '": ' + \
                         self.logentries[i].simplejson() + ",\n"
        
        return output[:-2] + "\n}"


    def rmlogentry(self, logentry):
        """Remove a logentry from the relation table"""
        self.logentries.remove(logentry)

        return self


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


    def username_list(self):
        """Return all the direct users names of the target"""
        usernames = []

        for user in self.members:
            usernames.append(user.show_name())

        return usernames
    

    def username_list_json(self):
        """Return all the direct users names of the target"""
        usernames = ""

        for user in self.members:
            usernames = usernames + \
                        "{\"Name\" : \"" + user.show_name() + "\"," + \
                        "\"Comment\" : \"" + user.show_comment() + "\"},"

        return usernames[:-1]


    def user_list(self):
        """Return all the direct users of the target"""
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
        """Return all the users of the target's usergroups"""
        Users = {}

        return Users


    def usergroupname_list(self):
        """Return all the direct usergroups' names of the target"""
        usergroupnames = []

        for usergroup in self.gmembers:
            usergroupnames.append(usergroup.show_name())

        return usergroupnames


    def usergroupname_list_json(self):
        """Return all the direct usergroups' names of the target json way"""
        usergroupnames = ""

        for usergroup in self.gmembers:
            usergroupnames = usergroupnames + "{\"Name\" : \"" + \
                             usergroup.show_name() + "\"," + \
                             "\"Comment\" : \"" + \
                             usergroup.show_comment() + "\"},"

        return usergroupnames[:-1]


    def usergroup_list(self):
        """Return all the direct usergroups of the target"""
        usergroups = []

        for usergroup in self.gmembers:
            usergroups.append(usergroup)

        return usergroups


    # Targetgroup management
    def targetgroup_list(self):
        """Return a list of all targetgroups which contain
        this target
        """
        targetgroups = []

        query = db.session.query(
            targetgroup.Targetgroup).order_by(
            targetgroup.Targetgroup.name).all()

        for each_targetgroup in query:
            if self.name in each_targetgroup.all_targetname_list():
                targetgroups.append(each_targetgroup)

        return targetgroups

    # Access management
    def list_all_usernames(self):
        """Return a list with all the users who can access
        this target
        """
        usernames = self.username_list()

        for usergroup in self.usergroup_list():
            for username in usergroup.all_username_list():
                if username not in usernames:
                   usernames.append(username)

        for targetgroup in self.targetgroup_list():
            for username in targetgroup.all_username_list():
                if username not in usernames:
                    usernames.append(username)

        return usernames


    def list_all_usergroupnames(self):
        """Return a list with all the usergroups who can access
        this target
        """
        usergroupnames = self.usergroupname_list()

        for usergroup in self.usergroup_list():
            for subusergroupname in usergroup.all_usergroupname_list():
                if subusergroupname not in usergroupnames:
                   usergroupnames.append(subusergroupname)

        return usergroupnames


    def list_all_targetgroupnames(self):
        """Return a list with all the targetgroups which contain
        this target
        """
        targetgroupnames = []

        query = db.session.query(
            targetgroup.Targetgroup).order_by(
            targetgroup.Targetgroup.name).all()

        for each_targetgroup in query:
            if self.name in each_targetgroup.all_targetname_list():
                targetgroupnames.append(each_targetgroup.show_name())

        return targetgroupnames


    def direct_targetgroups(self):
        """Return the list of the directly attached targetgroups"""
        return self.memberoftg


    def dayssinceconnection(self):
        """Return the number of days since this target hasn't been used"""
        # Look for a log entry with this target
        lastuse = ""
        if self.logentries:
            lastuse = self.logentries[-1].connectiondate
            
        if lastuse != "":
            date = datetime.strptime(lastuse, '%Y%m%dT%H%M%S')
            today = date.today()
            numberofdays = today - date
            return int(numberofdays.days)
        else:
            return int(-1)

