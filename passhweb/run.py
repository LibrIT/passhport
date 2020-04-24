#!flask/bin/python

from app import app
import config

app.config['SECRET_KEY'] = "bsqdttyqiuceccmcmpgg"
app.run(debug=config.DEBUG, host=config.HOSTNAME, port=int(config.PORT))


