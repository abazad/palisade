'''
Created on Jul 16, 2013

@author: bova
'''
from flask import render_template, request
from palisade.ui.admin import admin
from palisade.db.schema import SQ_User
from palisade.db.conn import Session

@admin.route('/', defaults={'page': 'index'})
@admin.route('/user')
def show_users():
    session = Session()
    users = session.query(SQ_User).all()
            
    return render_template('show_users.html', users=users)


