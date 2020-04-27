from flask import Flask
from flask_login import LoginManager, login_required

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from app import views

