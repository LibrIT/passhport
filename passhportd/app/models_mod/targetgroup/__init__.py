# -*-coding:Utf-8 -*-

from app import db

"""Targetgroup defines a group of targets (can contain some targetgroups too)"""
class Targetgroup(db.Model):
    __tablename__   = "targetgroup"
    id              = db.Column(db.Integer,     primary_key = True)
    targetgroupname = db.Column(db.String(256), index = True, unique = True)
    comment         = db.Column(db.String(500), index = True, unique = False)

    def __repr__(self):
        """Return main data of the targetgroup as a string"""
        output = []

        output.append("Targetgroupname: {}".format(self.targetgroupname.encode('utf8')))

        if self.comment:
            output.append("Comment: {}".format(self.comment.encode('utf8')))

        return "\n".join(output)
