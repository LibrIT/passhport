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

    # Relations
    targets = db.relationship("Target", secondary="target_user")


    def __repr__(self):
        """Return main data of the user as a string"""
        output = []

        output.append("Name: {}".format(self.name))
        output.append("SSH key: {}".format(self.sshkey))
        output.append("Comment: {}".format(self.comment))
        output.append("Accessible target list: " + \
            " ".join(self.accessible_targetname_list()))
        output.append("Accessible targets:\n" + \
            "".join(self.all_access()))

        return "\n".join(output)


    def show_name(self):
        """Return a string containing the user's name"""
        return self.name


    def accessible_targetname_list(self):
        """Return target names which are accessible to the user"""
        targetnames = []

        query = db.session.query(
            target.Target).order_by(
            target.Target.name).all()

        for each_target in query:
            if self.name in each_target.list_all_usernames():
                targetnames.append(each_target.show_name())

        return targetnames


    def accessible_target_list(self):
        """Return target objects which are accessible to the user"""
        targets = []

        query = db.session.query(
            target.Target).order_by(
            target.Target.name).all()

        for each_target in query:
            if self.name in each_target.list_all_usernames():
                targets.append(each_target)

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


    def all_access(self):
        """Return a detailled view of the path to the differents targets"""
        targetspaths = []

        #First list the targets where the user is directly attached
        #We will check all the accessible targets, let list them
        accessible_targets = self.accessible_target_list()
        if accessible_targets:
            targetspaths.append("Directly attached: \n")
            for each_target in accessible_targets:
                if self in each_target.user_list():
                    targetspaths.append(each_target.name + "\n")

        #Secondly list all the target the user can access through his groups
        #So we need to list all the groups the user is in
        my_usergroups = self.direct_usergroups()

        for each_usergroup in my_usergroups:
            targetspaths.append("".join(each_usergroup.show_targets(0)) + "\n")

        #Finaly the targetgroups the user is in
        my_targetgroups = self.direct_targetgroups()
        for each_targetgroup in my_targetgroups:
            targetspaths.append("".join(each_targetgroup.show_targets(0)))

        return targetspaths
