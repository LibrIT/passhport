# -*-coding:Utf-8 -*-

from app import db

"""Usergroup defines a group of users (can contain some usergroups too)"""
class Usergroup(db.Model):
    __tablename__ = "usergroup"
    id            = db.Column(db.Integer,     primary_key = True)
    usergroupname = db.Column(db.String(256), index = True, unique = True)
    comment       = db.Column(db.String(500), index = True, unique = False)

    # Relations
    members = db.relationship("User", secondary = "group_user")

    def __repr__(self):
        """Return main data of the usergroup as a string"""
        output = []

        output.append("Usergroupname: {}".format(self.usergroupname.encode("utf8")))
        output.append("Comment: {}".format(self.comment.encode("utf8")))

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
        """Return true if the given user is a member of the target, false otherwise"""
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
