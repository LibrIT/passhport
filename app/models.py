from app import db
from .models_mod import user, target, usergroup, targetgroup

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

