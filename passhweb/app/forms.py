from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms.widgets import TextArea
import config

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    

class TargetForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    if config.DBP:
        choices = [('ssh', 'SSH'),
                   ('mysql', 'MySQL'),
                   ('oracle', 'Oracle'),
                   ('postgresql', 'PostgreSQL')]
    else:
        choices = [('ssh', 'SSH')]
    targettype = SelectField('targettype', choices = choices,
                             default = ("ssh", "SSH"))
    hostname = StringField('hostname', validators=[DataRequired()])
    login = StringField('login', validators=[])
    port = IntegerField('port', validators=[NumberRange(min=0, max=7200)])
    sessiondur = IntegerField('sesssiondur', validators=[NumberRange(min=0, max=7200)])
    sshoptions = StringField('sshoptions', validators=[])
    comment = StringField('comment', validators=[])
    changepwd = BooleanField('changepwd', default=False)
    

class UserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    sshkey = StringField('sshkey', widget=TextArea(), 
                         validators=[DataRequired()])
    comment = StringField('comment', validators=[])
    logfilesize = IntegerField('logfilesize', validators=[NumberRange(min=0, max=65535), Optional()])


class UsergroupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    comment = StringField('comment', validators=[])


class TargetgroupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    comment = StringField('comment', validators=[])


class ConfigForm(FlaskForm):
    url = StringField('url', validators=[DataRequired()])
    sslkey =  StringField('sslkey', validators=[DataRequired()])
    sslcert =  StringField('sslcert', validators=[DataRequired()])
    privsshkey =  StringField('privsshkey', validators=[DataRequired()])
    pubsshkey =  StringField('pubsshkey', validators=[DataRequired()])
