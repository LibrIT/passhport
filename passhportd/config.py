"""
    Configuration file
"""
import os

"""
    Database (sqlite by default)
"""
basedir = os.path.expanduser('~')
datadir = os.path.join(basedir, 'var')

SQLALCHEMY_DATABASE_DIR = datadir
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(datadir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(datadir, 'db_repository')
