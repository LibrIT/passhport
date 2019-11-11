# -*-coding:Utf-8 -*-
from app import app, db
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64, os
import config
   
class Passentry(db.Model):
    """Passentry store root password history for furture reference"""
    __tablename__ = "passentry"
    id = db.Column(db.Integer, primary_key=True)
    connectiondate = db.Column(db.String(20), index=True)
    password       = db.Column(db.LargeBinary(500), index=False)
    salt           = db.Column(db.LargeBinary(500), index=False)

    # Relations
    target = db.relationship("Target", secondary="target_pass")


    def __init__(self, connectiondate, password):
        self.connectiondate = connectiondate
        self.salt = os.urandom(16)
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
        return self.generatefernet().encrypt(password.encode())


    def decryptpassword(self):
        """Decrypt the password"""
        return self.generatefernet().decrypt(self.password).decode()


    def generatefernet(self):
        """Return a fernet object used to encrypt/decrypt the password"""
        kdf = PBKDF2HMAC(
                algorithm = hashes.SHA256(),
                length = 32,
                salt = self.salt,
                iterations = 100000,
                backend = default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(config.SALT.encode()))
        return Fernet(key)


