from app import db

"""
    Target defines informations for every servers accessible through passhport
"""
class Target(db.Model):
    __tablename__ = 'target'
    id          = db.Column(db.Integer,     primary_key=True)
    targetname  = db.Column(db.String(256), index=True,     unique=True)
    hostname    = db.Column(db.String(120), index=True,     nullable=False)
    port        = db.Column(db.Integer,     index=False)
    sshoptions  = db.Column(db.String(500), index=True)
    servertype  = db.Column(db.String(64),  index=True)
    autocommand = db.Column(db.String(128), index=True)
    comment     = db.Column(db.String(500), index=True)
    # Relations
    members     = db.relationship('User', 
                        secondary='target_user')
    gmembers    = db.relationship('Usergroup', 
                        secondary='target_group')

    def __repr__(self):
        # This is represented by all data in it
        output ="""Targetname: %s\n""" \
                    % (str(self.targetname).encode('utf8'))
        output = output + """Hostname: %s\n""" \
                    % (str(self.hostname).encode('utf8'))
        output = output + """Port: %s\n""" \
                    % (str(self.port).encode('utf8'))
        output = output + """Sshoptions: %s\n""" \
                    %(str(self.sshoptions).encode('utf8'))
        output = output + """Servertype: %s\n""" \
                    %(str(self.servertype).encode('utf8'))
        output = output + """Autocommand: %s\n""" \
                    %(str(self.autocommand).encode('utf8'))

        # Return comment only if it exist
        if isinstance(self.comment, basestring):
            output = output + """Comment: %s\n""" \
                    % (self.comment.encode('utf8'))

        return output

    """ User management """
    def adduser(self, user):
        # Add a user to the relation table
        if not self.is_member(user):
            self.members.append(user)
        return self

    def rmuser(self, user):
        # Remove all user entries from the target
        if self.is_member(user):
            self.members.remove(user)
        return self

    def is_member(self, user):
        return user in self.members

    """ Usergroup management """
    def addgroup(self, usergroup):
        if not self.is_gmember(usergroup):
            self.gmembers.append(usergroup)
        return self

    def rmgroup(self, usergroup):
        if self.is_gmember(usergroup):
            self.gmembers(usergroup)
        return self

    def is_gmember(self, usergroup):
        return usergroup in self.members

