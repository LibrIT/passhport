from app import db

"""
    Target defines informations for every servers accessible through passhport
"""
class Target(db.Model):
    
    id          = db.Column(db.Integer,     primary_key=True)
    targetname        = db.Column(db.String(256), index=True,     unique=True)
    hostname    = db.Column(db.String(120), index=True,     nullable=False)
    port        = db.Column(db.Integer,     index=False)
    sshoptions  = db.Column(db.String(500), index=True)
    servertype  = db.Column(db.String(64),  index=True)
    autocommand = db.Column(db.String(128), index=True)
    comment     = db.Column(db.String(500), index=True)

    def __repr__(self):
        # This is represented by all data in it
        output ="""Targetname: %s\n""" % (self.targetname.encode('utf8'))
        output = output + """Hostname: %s\n""" % (self.hostname.encode('utf8'))
        output = output + """Port: %i\n""" % (self.port)
        output = output + """Sshoptions: %s\n""" \
                %(self.sshoptions.encode('utf8'))
        output = output + """Servertype: %s\n""" \
                %(self.servertype.encode('utf8'))
        output = output + """Autocommand: %s\n""" \
                %(self.autocommand.encode('utf8'))

        # Return comment only if it exist
        if isinstance(self.comment, basestring):
            output = output + """Comment: %s\n""" \
                    % (self.comment.encode('utf8'))

        return output

