from app import db

"""
    Usergroup define a group of users (can contain some usergroups too)
"""
class Usergroup(db.Model):
    
    id      = db.Column(db.Integer,     primary_key=True)
    name    = db.Column(db.String(256), index=True,     unique=True)
    comment = db.Column(db.String(500), index=True,     unique=False)

    def __repr__(self):
        return '<Usergroup %r>' % (self.name)

