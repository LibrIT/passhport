# -*-coding:Utf-8 -*-

# Compatibility 2.7-3.4
from __future__ import absolute_import
from __future__ import unicode_literals

from app import app, db
from app.models_mod import target,usergroup,targetgroup,user
   
class Logentry(db.Model):
    """Logentry store connection history for furture reference"""
    __tablename__ = "logentry"
    id = db.Column(db.Integer, primary_key=True)
    pid            = db.Column(db.Integer, index=True)
    connectiondate = db.Column(db.String(20), index=True)
    endsessiondate = db.Column(db.String(20), index=True)
    connectioncmd  = db.Column(db.String(200), index=True)
    logfilepath    = db.Column(db.String(200)) # Empty if archived or logrotated
    logfilename    = db.Column(db.String(200), nullable=False)

    # Relations
    target = db.relationship("Target", secondary="target_log")
    user   = db.relationship("User", secondary="user_log")

    def __repr__(self):
        """Return main data of the Log entry as a string"""
        output = []

        output.append("Start date: {}".format(self.connectiondate))
        output.append("End date  : {}".format(self.endsessiondate))
        output.append("PID       : {}".format(str(self.pid)))
        output.append("Command   : {}".format(self.connectioncmd))
        output.append("Logfile:" + self.logfilepath + self.logfilename)
        output.append("User      : {}".format(self.user[0].show_name()))
        output.append("Target    : {}".format(self.target[0].show_name()))
        return "\n".join(output)


    def simplejson(self):
        """Return a json of logentry infos"""
        output = "{"
        output = output + "\"Start date\": \"" + format(self.connectiondate) + "\",\n"
        output = output + "\"End date\": \"" + \
                          format(self.show_endsessiondate()) + "\",\n"
        output = output + "\"Command\": \"" + \
                          format(self.connectioncmd) + "\",\n"
        output = output + "\"PID\": \"" + format(str(self.pid)) + "\",\n"
        output = output + "\"Logfile\": \"" + self.logfilepath + \
                          self.logfilename + "\",\n"
        output = output + "\"User\": \"" + format(self.user[0].show_name()) + "\",\n"
        output = output + "\"Target\": \"" + format(self.target[0].show_name()) + "\""
        output = output + "}"

        return output


    def setenddate(self, enddate):
        """Add a enddate at the moment this is called"""
        self.endsessiondate = enddate
        return True

    def show_endsessiondate(self):
        """Return "Connected" if not ended"""
        if self.endsessiondate:
            return self.endsessiondate
        return "Connected"
