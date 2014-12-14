from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

#Initialize Flask application
app = Flask(__name__)
app.config.from_object('config')
#Initialize database
db = SQLAlchemy(app)

from app import views, models
