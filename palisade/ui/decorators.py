'''
Created on 19.08.2013

@author: bova
'''

from functools import wraps
from flask import request, redirect, url_for, session, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('current_user') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('is_admin') == False:
            flash('You must be an admin!')
            return redirect(url_for('user.show_user'))
        return f(*args, **kwargs)
    return decorated_function