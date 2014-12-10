#!/usr/bin/env python

from flask import Blueprint
targetgroup = Blueprint('targetgroup', __name__)

@targetgroup.route("/targetgroup/list")
def targetgroup_list():
        return "list of targetgroups"


