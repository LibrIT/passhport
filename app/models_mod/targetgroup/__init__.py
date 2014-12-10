from app import db

"""
    Targetgroup contains targets (can contain some targetgroups too)
"""
class Targetgroup(db.Model):
    
    id      = db.Column(db.Integer,     primary_key=True)
    name    = db.Column(db.String(256), index=True,     unique=True)
    comment = db.Column(db.String(500), index=True,     unique=False)

    def __repr__(self):
        return '<Targetgroup %r>' % (self.name)

