#!/usr/bin/env python
# -*-coding:Utf-8 -*-
import os.path

from flask_migrate import stamp

from app import app, db
from config import SQLALCHEMY_DATABASE_DIR


if not os.path.exists(SQLALCHEMY_DATABASE_DIR):
    os.makedirs(SQLALCHEMY_DATABASE_DIR)

with app.app_context():
    db.create_all()
    # Mark the DB at the latest Alembic revision after creating tables.
    stamp(revision="head")
