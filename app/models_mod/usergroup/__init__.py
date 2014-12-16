from app import db

"""
    Usergroup define a group of users (can contain some usergroups too)
"""
class Usergroup(db.Model):
    __tablename__ = "usergroup"
    id          = db.Column(db.Integer,     primary_key=True)
    groupname   = db.Column(db.String(256), index=True,     unique=True)
    comment     = db.Column(db.String(500), index=True,     unique=False)
    # Relations
    members     = db.relationship('Target', 
                        secondary='target_group')

    def __repr__(self):
        # This is represented by all data in it
        output ="""Groupname: %s\n""" \
                    % (str(self.groupname).encode('utf8'))

        # Return comment only if it exist
        if isinstance(self.comment, basestring):
            output = output + """Comment: %s\n""" \
                    % (self.comment.encode('utf8'))

        return output

