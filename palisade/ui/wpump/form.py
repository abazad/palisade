'''
Created on 15.04.2013

@author: bova
'''

from wtforms import Form, TextField, validators

class DownloadForm(Form):
    url = TextField('Url', [validators.Required()])
    email = TextField('JabberID (like: user@fido.uz)', [validators.Required()])
    

