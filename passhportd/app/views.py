from app import app
from .views_mod import user, usergroup, target, targetgroup

@app.route('/')
def imalive():
        return """Passhport is running, gratz!"""
