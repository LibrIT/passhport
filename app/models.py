from app import db

"""
    User defines informations for every adminsys using passhport
"""
class User(db.Model):
    
    id      = db.Column(db.Integer,     primary_key=True)
    name    = db.Column(db.String(256), index=True)
    email   = db.Column(db.String(120), index=True,     unique=True,
                                                        nullable=False)
    sshkey  = db.Column(db.String(500), index=False,    unique=True,
                                                        nullable=False)
    comment = db.Column(db.String(500), index=True)

    def __repr__(self):
        return '<User %r>' % (self.name)


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


"""
    Usergroup define a group of users (can contain some usergroups too)
"""
class Usergroup(db.Model):
    
    id      = db.Column(db.Integer,     primary_key=True)
    name    = db.Column(db.String(256), index=True,     unique=True)
    comment = db.Column(db.String(500), index=True,     unique=False)

    def __repr__(self):
        return '<Usergroup %r>' % (self.name)


"""
    Targetgroup contains targets (can contain some targetgroups too)
"""
class Targetgroup(db.Model):
    
    id      = db.Column(db.Integer,     primary_key=True)
    name    = db.Column(db.String(256), index=True,     unique=True)
    comment = db.Column(db.String(500), index=True,     unique=False)

    def __repr__(self):
        return '<Targetgroup %r>' % (self.name)

###############################################################################
# Relations tables
###############################################################################
"""
    User_Target authorized access between users and targets (not including
                groups).
"""
class User_Target(db.Model):

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
    target_id   = db.Column(db.Integer, db.ForeignKey('target.id'))
    
    def __repr__(self):
        return '<User_Target %r>' % (self.id)


"""
    User_Group users in groups
"""
class User_Group(db.Model):

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id    = db.Column(db.Integer, db.ForeignKey('group.id'))
    
    def __repr__(self):
        return '<User_Group %r>' % (self.id)


"""
    Target_Group Targets a group can access
"""
class Target_Group(db.Model):

    id          = db.Column(db.Integer, primary_key=True)
    target_id   = db.Column(db.Integer, db.ForeignKey('target.id'))
    group_id    = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __repr__(self):
        return '<Target_Group %r>' % (self.id)


"""
    Target_Tgroup Targets in targetgroups
"""
class Target_TGroup(db.Model):

    id          = db.Column(db.Integer, primary_key=True)
    target_id   = db.Column(db.Integer, db.ForeignKey('target.id'))
    tgroup_id   = db.Column(db.Integer, db.ForeignKey('targetgroup.id'))

    def __repr__(self):
        return '<Target_TGroup %r>' % (self.id)


"""
    Group_Group Group in group (a group can contain multiple subgroups)
"""
class Group_Group(db.Model):

    id                  = db.Column(db.Integer, primary_key=True)
    group_id            = db.Column(db.Integer, db.ForeignKey('group.id'))
    containergroup_id   = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __repr__(self):
        return '<Group_Group %r>' % (self.id)


"""
    Tgroup_Tgroup Targets a group can access
"""
class Tgroup_Tgroup(db.Model):

    id                      = db.Column(db.Integer, primary_key=True)
    targetgroup_id          = db.Column(db.Integer, 
                                        db.ForeignKey('targetgroup.id'))
    containertargetgroup_id = db.Column(db.Integer, 
                                        db.ForeignKey('targetgroup.id'))

    def __repr__(self):
        return '<Tgroup_Tgroup %r>' % (self.id)


"""
    Tgroup_Group Targets in target group a group can access
"""
class Tgroup_Group(db.Model):

    id              = db.Column(db.Integer, primary_key=True)
    targetgroup_id  = db.Column(db.Integer, db.ForeignKey('targetgroup.id'))
    group_id        = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __repr__(self):
        return '<Tgroup_Group %r>' % (self.id)

