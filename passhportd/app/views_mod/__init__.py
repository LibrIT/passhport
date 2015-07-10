import flask
from app import app

@app.errorhandler(404)
def page_not_found(error):
    return "ERROR: You must fill the requested fields", 404
