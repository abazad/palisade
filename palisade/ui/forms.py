'''
Created on 24.07.2013

@author: bova
'''

from wtforms import Form, TextField, PasswordField, IntegerField, HiddenField, validators

class LoginForm(Form):
    login = TextField('Login', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

class UserForm(Form):
    id = HiddenField('Id')
    first_name = TextField('First Name', [validators.Required()])
    last_name = TextField('Last Name', [validators.Required()])
    login = TextField('Login', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    password_confirm = PasswordField('Password confirmation', 
                                     [validators.Required()])
    traffic_limit = IntegerField('Limit MB')
    