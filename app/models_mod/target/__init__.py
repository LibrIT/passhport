from app import db

"""
    Target defines informations for every servers accessible through passhport
"""
class Target(db.Model):
    
    id          = db.Column(db.Integer,     primary_key=True)
    name        = db.Column(db.String(256), index=True,     unique=True)
    hostname    = db.Column(db.String(120), index=True,     nullable=False)
    port        = db.Column(db.Integer,     index=False)
    sshoptions  = db.Column(db.String(500), index=True)
    servertype  = db.Column(db.String(64),  index=True)
    autocommand = db.Column(db.String(128), index=True)
    comment     = db.Column(db.String(500), index=True)

    def __repr__(self):
        return '<Target %r>' % (self.name)

