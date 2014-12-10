from app import app

@app.route('/')
def imalive():
        return """Passhport is running, gratz!"""

