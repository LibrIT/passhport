from flask import render_template, flash, redirect, session, url_for
from app import app
from app import forms as f
from flask import request
import requests
import config

### Routes ###
@app.route('/')
@app.route('/index')
def genconfig():
    # Cofiguration generation,
    form = f.ConfigForm()

    if request.method == "POST":
        #Prepare different files
        writeonfile(request.form["pubsshkey"], config.PUBSSH)
        writeonfile(request.form["privsshkey"], config.PRIVSSH)
        writeonfile(request.form["sslkey"], config.SSLKEY)
        writeonfile(request.form["sslcert"], config.SSLCERT)
        app.logger.error(request.form)
        return redirect(url_for('index'))

    # GET
    return render_template('pages/firstconfig.html',
                            pagename = "Configuration",
                            userid = "passhadmin",
                            superadmin = True,
                            form = form)


