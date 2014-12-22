from app import db

"""
    User defines informations for every adminsys using passhport
"""
class User(db.Model):
    __tablename__ = 'user'
    id      = db.Column(db.Integer,     primary_key=True)
    username= db.Column(db.String(256), index=True,     unique=True,
                                                        nullable=False)
    email   = db.Column(db.String(120), index=True,     unique=True)
    sshkey  = db.Column(db.String(500), index=False,    unique=True,
                                                        nullable=False)
    comment = db.Column(db.String(500), index=True)

    # Relations
    targets = db.relationship('Target',
                    secondary='target_user')

    def __repr__(self):
        # This is represented by all data in it
        output="""Username: %s\n""" % (self.username.encode('utf8'))
        # Return email only if it exist
        if isinstance(self.email, basestring):
            output = output + """Email: %s\n""" % (self.email.encode('utf8'))

        output = output + """Sshkey: %s\n""" % (str(self.sshkey).encode('utf8'))

        # Return comment only if it exist
        if isinstance(self.comment, basestring):
            output = output + """Comment: %s\n""" \
                    % (self.comment.encode('utf8'))

        return output

