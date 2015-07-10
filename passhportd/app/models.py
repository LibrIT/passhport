# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import db
from .models_mod import user, target, usergroup, targetgroup

###############################################################################
# Relations tables
###############################################################################
"""TargetUser authorized access between users and targets (not including groups)."""


class Target_User(db.Model):
    __tablename__ = "target_user"
    target_id = db.Column(
        db.Integer,
        db.ForeignKey("target.id"),
        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

"""Groupuser users in groups"""


class Group_User(db.Model):
    __tablename__ = "group_user"
    group_id = db.Column(
        db.Integer,
        db.ForeignKey("usergroup.id"),
        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

"""TargetGroup targets a group can access"""


class Target_Group(db.Model):
    __tablename__ = "target_group"
    target_id = db.Column(
        db.Integer,
        db.ForeignKey("target.id"),
        primary_key=True)
    group_id = db.Column(
        db.Integer,
        db.ForeignKey("usergroup.id"),
        primary_key=True)


class TGroup_User(db.Model):

    """Targetgroups contain several users"""
    __tablename__ = "tgroup_user"
    targetgroup_id = db.Column(
        db.Integer,
        db.ForeignKey("targetgroup.id"),
        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)

"""TgroupTarget targets in targetgroups"""


class TGroup_Target(db.Model):
    __tablename__ = "tgroup_target"
    tgroup_id = db.Column(
        db.Integer,
        db.ForeignKey("targetgroup.id"),
        primary_key=True)
    target_id = db.Column(
        db.Integer,
        db.ForeignKey("target.id"),
        primary_key=True)

"""TgroupTgroup Targets a group can access"""


class TGroup_TGroup(db.Model):
    __tablename__ = "tgroup_tgroup"
    targetgroup_id = db.Column(
        db.Integer,
        db.ForeignKey("targetgroup.id"),
        primary_key=True)
    containertargetgroup_id = db.Column(
        db.Integer,
        db.ForeignKey("targetgroup.id"),
        primary_key=True)

"""TgroupGroup Targets in target group a group can access"""


class Tgroup_Group(db.Model):
    __tablename__ = "tgroup_group"
    targetgroup_id = db.Column(
        db.Integer,
        db.ForeignKey("targetgroup.id"),
        primary_key=True)
    group_id = db.Column(
        db.Integer,
        db.ForeignKey("usergroup.id"),
        primary_key=True)
