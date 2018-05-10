# -*-coding:Utf-8 -*-
from app import app, db
from app.models_mod import target
from simplecrypt import encrypt, decrypt
import config
   
class Passentry(db.Model):
    """Passentry store root password history for furture reference"""
    __tablename__ = "passentry"
    id = db.Column(db.Integer, primary_key=True)
    connectiondate = db.Column(db.String(20), index=True)
    password       = db.Column(db.String(200), index=True)

    # Relations
    target = db.relationship("Target", secondary="target_pass")


    def __init__(self, connectiondate, password):
        self.connectiondate = connectiondate
        self.password = self.encryptpassword(password)
    

    def __repr__(self):
        """Return main data of the passentry as a string"""
        output = []

        output.append("Date    : {}".format(self.connectiondate))
        output.append("Password: {}".format(self.decryptpassword()))
        output.append("Target  : {}".format(self.target[0].show_name()))
        return "\n".join(output)


    def notargetjson(self):
        """Return a json of passentry infos except target name"""
        output = "{"
        output = output + "\"date\": \"" + format(self.connectiondate) + "\",\n"
        output = output + "\"password\": \"" + \
                          format(self.decryptpassword()) + "\""
        output = output + "}"

        return output


    def encryptpassword(self, password):
        """Encrypt the password"""
        return password
        return encrypt(config.SALT, password)


    def decryptpassword(self):
        """Decrypt the password"""
        return self.password
        return decrypt(config.SALT, self.password).decode('utf8')
