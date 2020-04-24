from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, username):
        self.id = username

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # python 3

    def get(id):
        return User(id)

    def __repr__(self):
        return '<User %r>' % (self.id)
