# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import db
from .models_mod import user, target, usergroup, targetgroup, logentry, exttargetaccess

###############################################################################
# Relations tables
###############################################################################
class Target_Log(db.Model):
    """Link between a connexion and a target"""
    __tablename__ = "target_log"
    target_id = db.Column(
        db.Integer,
        db.ForeignKey("target.id"),
        primary_key=True)
    logentry_id = db.Column(
        db.Integer,
        db.ForeignKey("logentry.id"),
        primary_key=True)


class User_Log(db.Model):
    """Link between a connexion and a user"""
    __tablename__ = "user_log"
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        primary_key=True)
    logentry_id = db.Column(
        db.Integer,
        db.ForeignKey("logentry.id"),
        primary_key=True)

    
class Target_Extaccess(db.Model):
    """Link between an access demand and a target"""
    __tablename__ = "target_extaccess"
    target_id = db.Column(
        db.Integer,
        db.ForeignKey("target.id"),
        primary_key=True)
    exttargetaccess_id = db.Column(
        db.Integer,
        db.ForeignKey("exttargetaccess.id"),
        primary_key=True)


class User_Extaccess(db.Model):
    """Link between an access demand and a user"""
    __tablename__ = "user_extaccess"
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        primary_key=True)
    exttargetaccess_id = db.Column(
        db.Integer,
        db.ForeignKey("exttargetaccess.id"),
        primary_key=True)


class Target_User(db.Model):
    """TargetUser authorized access between users and targets
    (not including groups).
    """
    __tablename__ = "target_user"
    target_id = db.Column(
        db.Integer,
        db.ForeignKey("target.id"),
        primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        primary_key=True)


class Tg_admins(db.Model):
    """Users authorized to admin targetgroups"""
    __tablename__ = "tg_admins"
    target_id = db.Column(
        db.Integer,
        db.ForeignKey("targetgroup.id"),
        primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        primary_key=True)


class Ug_admins(db.Model):
    """Users authorized to admin usergroups"""
    __tablename__ = "ug_admins"
    target_id = db.Column(
        db.Integer,
        db.ForeignKey("usergroup.id"),
        primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        primary_key=True)


class Group_User(db.Model):
    """Groupuser users in groups"""
    __tablename__ = "group_user"
    group_id = db.Column(
        db.Integer,
        db.ForeignKey("usergroup.id"),
        primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        primary_key=True)


class Target_Group(db.Model):
    """TargetGroup targets a group can access"""
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
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        primary_key=True)


class TGroup_Target(db.Model):
    """TgroupTarget targets in targetgroups"""
    __tablename__ = "tgroup_target"
    tgroup_id = db.Column(
        db.Integer,
        db.ForeignKey("targetgroup.id"),
        primary_key=True)
    target_id = db.Column(
        db.Integer,
        db.ForeignKey("target.id"),
        primary_key=True)


class Tgroup_Group(db.Model):
    """TgroupGroup Targets in target group a group can access"""
    __tablename__ = "tgroup_group"
    targetgroup_id = db.Column(
        db.Integer,
        db.ForeignKey("targetgroup.id"),
        primary_key=True)
    group_id = db.Column(
        db.Integer,
        db.ForeignKey("usergroup.id"),
        primary_key=True)
