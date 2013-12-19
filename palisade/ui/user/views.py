'''
Created on 15.08.2013

@author: bova
'''
from flask import render_template, request, redirect, url_for, flash, g, session
from palisade.ui.user import user
from palisade.db.schema import SQ_User, SQ_Access_Log_Data, SQ_Lost_Password
from palisade.db.conn import Session
from sqlalchemy.sql import func
from datetime import date, datetime

from palisade.ui.decorators import login_required
from palisade.ui.forms import LostPasswordForm, EditPasswordForm
from palisade.utils import id_generator


@user.route('/', methods=['GET'])
@login_required
def show_user():
    db = Session()
    current_user = session.get('current_user')
    bytes_sum = {}
    user = db.query(SQ_User).filter(SQ_User.login==current_user).first()
    today = date.today()
    begin_of_month = date(year=today.year, month=today.month, day=1)
#    bytes = db.query(func.sum(SQ_Access_Log_Data.bytes))\
#                        .filter(SQ_Access_Log_Data.user_name==user.login)\
#                        .scalar()
    bytes = None
    bytes_sum['all'] = bytes and bytes or 0
                        
#    bytes = db.query(func.sum(SQ_Access_Log_Data.bytes))\
#                        .filter(SQ_Access_Log_Data.user_name==user.login)\
#                        .filter(SQ_Access_Log_Data.access_time>=begin_of_month)\
#                        .scalar()
    bytes = None
    bytes_sum['month'] = bytes and bytes or 0
                        
    bytes = db.query(func.sum(SQ_Access_Log_Data.bytes))\
                        .filter(SQ_Access_Log_Data.user_name==user.login)\
                        .filter(SQ_Access_Log_Data.access_time>=today)\
                        .scalar()
    bytes_sum['today'] = bytes and bytes or 0
    db.close()
    return render_template('user/show_user.html', user=user, bytes_sum=bytes_sum)

def is_email_exist(email):
    db = Session()
    user = db.query(SQ_User).filter(SQ_User.email==email).all()
    if len(user) > 0:
        return True
    return False

@user.route('/lost_password', methods=['GET', 'POST'])
def lost_password():
    form = LostPasswordForm(request.form)         
    if request.method == 'POST':
        if form.validate() and is_email_exist(form.email.data):
            lost_password = SQ_Lost_Password(datetime.now(), 
                                             form.email.data,
                                             'NEW',
                                             id_generator(32))   
            db = Session()
            db.add(lost_password)
            db.commit()
            flash('Check your mailbox in a few minutes!')
            return redirect(url_for('login'))
        else:
            flash("Invalid email or email doesn't exist")            
    return render_template('user/lost_password.html', form=form)

def is_recover_args_valid(secret_key, email):
    if secret_key and email:
        db = Session()
        lost_pwd = db.query(SQ_Lost_Password).\
                    filter(SQ_Lost_Password.secret_key==secret_key).\
                    first()
        db.close()
        if lost_pwd.email == email:
            return True
    return False

@user.route('/edit_password', methods=['GET', 'POST'])
def edit_password():
    form = EditPasswordForm(request.form)
    secret_key = request.args.get('secret_key')
    email = request.args.get('email')    
    if request.method == 'GET' and is_recover_args_valid(secret_key, email):
        session['secret_key'] = secret_key
        session['email'] = email    
        return render_template('user/edit_password.html', form=form)
    elif request.method == 'POST' and form.validate():
        db = Session()
        user = db.query(SQ_User).filter(SQ_User.email==session.get('email')).first()
        user.password = form.password.data
        lost_pwds = db.query(SQ_Lost_Password).\
                    filter(SQ_Lost_Password.email==session.get('email'))
        for lost_pwd in lost_pwds:
            db.delete(lost_pwd)
        db.commit()
        flash('Your password updated successful!')
        session.pop('secret_key', None)
        session.pop('email', None)
        db.close()
        return redirect(url_for('login'))
    else:
        flash('Your password recovery code is invalid')
        return redirect(url_for('login'))