# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask application
app = Flask(__name__)
app.config.from_object("config")

# Initialize database
db = SQLAlchemy(app)

from app import views, models
