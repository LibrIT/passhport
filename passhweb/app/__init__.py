from flask import Flask
import config

app = Flask(__name__)

if config.FIRSTLAUNCH == True:
    from app import firstlaunch
else:
    from flask_login import LoginManager
    from flask_login import login_required
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    from app import views

