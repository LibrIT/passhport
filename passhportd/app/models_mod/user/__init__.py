# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import app, db
from app.models_mod import target,usergroup,targetgroup
   
class User(db.Model):
    """User defines information for every adminsys using passhport"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    sshkey = db.Column(
        db.String(500),
        index=False,
        unique=True,
        nullable=False)
    comment = db.Column(db.String(500), index=True)


    # Relations (in targetgroups)
    targets = db.relationship("Target", secondary="target_user")
    usergroups = db.relationship("Usergroup", secondary="group_user")
    targetgroups = db.relationship("Targetgroup", secondary="tgroup_user")
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

        return "\n".join(output)

    def simplejson(self):
        """Return a simplified data of the user as json but not all the data"""
        output = "{\n"

        output = output + "\"email\": \"" + format(self.name) + "\",\n"
        output = output + "\"sshkey\": \"" + format(self.sshkey) + "\",\n"
        output = output + "\"comment\": \"" + format(self.comment) + "\",\n"
        output = output + "\"accessibleTargetList\": \"" + format(self.accessible_targetname_list()) + "\",\n"
        #output = output + "\"accessibleTargets\": \"" + format(self.accessible_target_list("json")) + "\"\n"
        output = output + "}"

        return output

    def show_name(self):
        """Return a string containing the user's name"""
        return self.name


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
            for target in usergroup.accessible_target_list():
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


    def direct_usergroups(self):
        """Return the list of the groups where the user is directly attached"""
        directusergroups  = []
        
        query = db.session.query(
            usergroup.Usergroup).order_by(
            usergroup.Usergroup.name).all()

        for each_usergroup in query:
            if self.name in each_usergroup.username_list():
                directusergroups.append(each_usergroup)

        return directusergroups


    def direct_targetgroups(self):
        """Return the list of the targetgroups with user directly attached"""
        directtargetgroups  = []
        
        query = db.session.query(
            targetgroup.Targetgroup).order_by(
            targetgroup.Targetgroup.name).all()

        for each_targetgroup in query:
            if self.name in each_targetgroup.username_list():
                directtargetgroups.append(each_targetgroup)

        return directtargetgroups

