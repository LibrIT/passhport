# -*-coding:Utf-8 -*-

from app import db

# Table to handle the self-referencing many-to-many relationship for the Usergroup class:
# First column holds the containers, the second the subgroups.
group_of_group = db.Table(
    'group_of_group',
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

"""Usergroup defines a group of users (can contain some usergroups too)"""


class Usergroup(db.Model):
    __tablename__ = "usergroup"
    id = db.Column(db.Integer, primary_key=True)
    usergroupname = db.Column(db.String(256), index=True, unique=True)
    comment = db.Column(db.String(500), index=True, unique=False)

    # Relations
    members = db.relationship("User", secondary="group_user")
    gmembers = db.relationship(
        "Usergroup",
        secondary=group_of_group,
        primaryjoin=id == group_of_group.c.container_id,
        secondaryjoin=id == group_of_group.c.subgroup_id,
        backref="containedin")

    def __repr__(self):
        """Return main data of the usergroup as a string"""
        output = []

        output.append(
            "Usergroupname: {}".format(
                self.usergroupname.encode("utf8")))
        output.append("Comment: {}".format(self.comment.encode("utf8")))
        output.append("User list:")

        for user in self.members:
            output.append(user.show_email())

        output.append("Usergroup list: ")

        for usergroup in self.gmembers:
            output.append(usergroup.show_usergroupname())

        return "\n".join(output)

    def show_usergroupname(self):
        """Return a string containing the usergroup's name"""
        return self.usergroupname.encode("utf8")

    def show_users(self):
        """Show user list of the usergroup"""
        output = []

        output.append("User list:")

        for user in self.members:
            output.append(user.show_email())

        return "\n".join(output)

    # User management
    def is_member(self, user):
        """Return true if the given user is a member of the usergroup, false otherwise"""
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

    def email_in_usergroup(self, email):
        """Return true if the given email belongs to a member of the usergroup"""
        for user in self.members:
            if user.show_email() == email:
                return True

        return False

    # Usergroup management
    def is_gmember(self, usergroup):
        """Return true if the given usergroup is a member of the usergroup, false otherwise"""
        return usergroup in self.gmembers

    def addusergroup(self, usergroup):
        """Add a usergroup to the relation table"""
        if not self.is_gmember(usergroup):
            self.gmembers.append(usergroup)

        return self

    def rmusergroup(self, usergroup):
        """Remove a usergroup from the relation table"""
        if self.is_gmember(usergroup):
            self.gmembers.remove(usergroup)

        return self
