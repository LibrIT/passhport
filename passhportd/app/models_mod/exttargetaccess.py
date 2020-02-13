# -*-coding:Utf-8 -*-
from app import app, db
from app.models_mod import target,user
   
class Exttargetaccess(db.Model):
    """Exttargetaccess store special targets access demands"""
    __tablename__ = "exttargetaccess"
    id = db.Column(db.Integer, primary_key=True)
    startdate = db.Column(db.String(50), index=True)
    stopdate  = db.Column(db.String(50), index=True)
    userip    = db.Column(db.String(20), index=True)
    proxy_ip  = db.Column(db.String(20), index=True)
    proxy_pid = db.Column(db.Integer, index=True, default=0) #0 means closed
    proxy_port= db.Column(db.Integer, index=True)

    # Relations
    target = db.relationship("Target", secondary="target_extaccess")
    user   = db.relationship("User", secondary="user_extaccess")

    def __repr__(self):
        """Return main data as a string"""
        output = []

        output.append("Start date : {}".format(self.startdate))
        output.append("Stop date : {}".format(self.stopdate))
        output.append("User IP : {}".format(self.userip))
        output.append("User   : {}".format(self.user[0].show_name()))
        output.append("Target : {}".format(self.target[0].show_name()))
        output.append("PID : {}".format(self.proxy_pid))
        return "\n".join(output)


    def simplejson(self):
        """Return a json of exttargetaccess infos"""
        output = "{"
        output = output + "\"Start date\": \"" + \
                          format(self.startdate) + "\",\n"
        output = output + "\"Stop date\": \"" + \
                          format(self.stopdate) + "\",\n"
        output = output + "\"User ip\": \"" + format(self.userip) + "\",\n"
        output = output + "\"User\": \"" + format(self.user[0].show_name()) + "\",\n"
        output = output + "\"Target\": \"" + format(self.target[0].show_name()) + "\""
        output = output + "}"

        return output


    def addtarget(self, target):
        self.target.append(target)
        return self
        

    def adduser(self, user):
        self.user.append(user)
        return self

    def show_username(self):
        if self.user:
            return self.user[0].show_name()
        return "None"


    def show_targetname(self):
        if self.target:
            return self.target[0].show_name()
        return "None"


    def set_proxy_pid(self, pid):
        self.proxy_pid = pid
        return self
