'''
Created on Jul 16, 2013

@author: bova
'''
from flask import render_template, request
from palisade.ui.admin import admin

@admin.route('/', defaults={'page': 'index'})
@admin.route('/user')
def show_users():
    return render_template('show_users.html')


