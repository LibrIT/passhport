# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals


from datetime import datetime, timedelta, date
from app import app, db
from app.models_mod import target,usergroup,targetgroup
   
class User(db.Model):
    """User defines information for every adminsys using passhport"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(120), 
                           index=True, unique=True, nullable=False)
    sshkey     = db.Column(db.String(500), 
                           index=False, unique=True, nullable=False)
    comment    = db.Column(db.String(500), index=True)
    superadmin = db.Column(db.Boolean, unique=False, default=False)


    # Relations (in targetgroups)
    targets      = db.relationship("Target", secondary="target_user")
    usergroups   = db.relationship("Usergroup", secondary="group_user")
    targetgroups = db.relationship("Targetgroup", secondary="tgroup_user")
    logentries   = db.relationship("Logentry", secondary="user_log")
    # Admins - can admin usergroups and targetgroups (add and remove users)
    adminoftg = db.relationship("Targetgroup", secondary="tg_admins")
    adminofug = db.relationship("Usergroup", secondary="ug_admins")


    def __repr__(self):
        """Return main data of the user as a string"""
        output = []

        output.append("Email: {}".format(self.name))
        output.append("SSH key: {}".format(self.sshkey))
        output.append("Comment: {}".format(self.comment))
        output.append("Accessible target list: " + \
            " ".join(self.accessible_targetname_list()))
        output.append("\nDetails in access:\n" + \
            "".join(self.accessible_target_list("details")))
        if self.superadmin:
            output.append("This user is a web interface superadmin")

        return "\n".join(output)


    def simplejson(self):
        """Return a simplified data of the user as json but not all the data"""
        output = "{\n"

        output = output + "\"email\": \"" + format(self.name) + "\",\n"
        output = output + "\"sshkey\": \"" + format(self.sshkey) + "\",\n"
        output = output + "\"comment\": \"" + format(self.comment) + "\",\n"
        output = output + "}"

        return output


    def show_name(self):
        """Return a string containing the user's name"""
        return self.name


    def show_comment(self):
        """Return a string containing the user's comment"""
        return self.comment


    def accessible_targetname_list(self):
        """Return target names which are accessible to the user"""
        return self.accessible_target_list("names")


    def accessible_target_list(self, style="object"):
        """Return targets accessible to the users (as object or names list)"""
        targets = []
        output = "Accessible directly: "

        # 1. list all the directly attached targets
        for target in self.targets:
            targets.append(target)
            output = output + target.show_name() + " ; "
        
        output = output + "\nAccessible through usergroups: "
        # 2. list all the targets accessible through usergroup
        for usergroup in self.usergroups:
            output = output + "\n" + usergroup.show_name() + ": "
            for target in usergroup.accessible_target_list(mode="obj"):
                output = output + target.show_name() + " ; "
                if target not in targets:
                    targets.append(target)

        output = output + "\nAccessible through targetgroups: "
        # 3. list all the targets accessible through targetgroup
        for targetgroup in self.targetgroups:
            output = output + "\n" + targetgroup.show_name() + ": "
            for target in targetgroup.accessible_target_list():
                output = output + target.show_name() + " ; "
                if target not in targets:
                    targets.append(target)


        # return target objects or names depending of style
        if style == "names":
            targetnames = []
            for target in targets:
                targetnames.append(target.show_name())
            targets = sorted(targetnames)
        elif style == "details":
            targets = output
        
        return targets


    def direct_targets(self):
        """Return the list of the targets where the user is directly attached"""
        return self.targets
        

    def direct_usergroups(self):
        """Return the list of the groups where the user is directly attached"""
        return self.usergroups


    def direct_targetgroups(self):
        """Return the list of the targetgroups with user directly attached"""
        return self.targetgroups


    def memberof(self, obj):
        """Return a string list of direct memberships of this user"""
        if obj == "target":
            members = self.targets
        elif obj == "targetgroup":
            members = self.targetgroups
        elif obj == "usergroup":
            members = self.usergroups
        else:
            return "Error in object type"
            
        ret = "["
        for m in members:
            ret = ret + m.name + ","
        return ret[:-1] + "]"


    def togglesuperadmin(self):
        """Change the superadmin flag"""
        self.superadmin = not self.superadmin

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


    def lastconnection(self):
        """Return the number of days since this account hasn't been used"""
        # Look for a log entry with this user
        lastuse = ""
        if self.logentries:
            lastuse = self.logentries[-1].connectiondate
            
        if lastuse != "":
            date = datetime.strptime(lastuse, '%Y%m%dT%H%M%S')
            today = date.today()
            numberofdays = today - dat
            return numberofdays.days
        else:
            return (-1)


