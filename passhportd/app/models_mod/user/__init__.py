# -*-coding:Utf-8 -*-

from app import db

"""User defines information for every adminsys using passhport"""


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
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

        output.append("Email: {}".format(self.email))
        output.append("SSH key: {}".format(self.sshkey))
        output.append("Comment: {}".format(self.comment))

        return "\n".join(output)

    def show_email(self):
        """Return a string containing the user's email"""
        return self.email.encode("utf8")
