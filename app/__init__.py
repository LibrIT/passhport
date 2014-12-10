from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from API.user import user
from API.target import target
from API.usergroup import usergroup
from API.targetgroup import targetgroup

#Initialize Flask application
app = Flask(__name__)
app.config.from_object('config')
#Define the objects APIs
app.register_blueprint(user)
app.register_blueprint(target)
app.register_blueprint(usergroup)
app.register_blueprint(targetgroup)
app.config.from_object('config')
#Initialize database
db = SQLAlchemy(app)

from app import views, models
