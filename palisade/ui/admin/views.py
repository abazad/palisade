'''
Created on Jul 16, 2013

@author: bova
'''
from flask import render_template, request, redirect, url_for, flash
from palisade.ui.admin import admin
from palisade.db.schema import SQ_User
from palisade.db.conn import Session
from palisade.ui.forms import UserForm

#@admin.route('/', defaults={'page': 'index'})
@admin.route('/user')
def show_users():
    session = Session()
    users = session.query(SQ_User).all()
            
    return render_template('show_users.html', users=users)

@admin.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = SQ_User(form.first_name.data,
                       form.last_name.data,
                       form.login.data,
                       form.password.data,                       
                       'A',
                       form.traffic_limit.data)
        session = Session()
        session.add(user)
        session.commit()
        flash("User successfully added!")
        return redirect(url_for('.show_users'))    
    return render_template('add_user.html', form=form)

#TODO: add feedback after form validate
@admin.route('/user/edit/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id=None):
    session=Session()
    user = session.query(SQ_User).filter(SQ_User.id==user_id).first()
    form = UserForm(request.form, user)
    if request.method == 'POST' and form.validate:
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.traffic_limit = form.traffic_limit.data
        session.commit()        
        return redirect(url_for('.show_users'))
    return render_template('edit_user.html', form=form)

@admin.route('/user/delete/<user_id>', methods=['GET'])
def delete_user(user_id):
    session = Session()
    user = session.query(SQ_User).filter(SQ_User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
        flash("User successfully deleted.")
    else:
        flash("User doesn't exist")    
    return redirect(url_for('.show_users'))

    
    