'''
Created on 15.08.2013

@author: bova
'''
from flask import render_template, request, redirect, url_for, flash, g, session
from palisade.ui.user import user
from palisade.db.schema import SQ_User, SQ_Access_Log_Data
from palisade.db.conn import Session
from sqlalchemy.sql import func
from datetime import date

@user.route('/', methods=['GET'])
def show_user():
    db = Session()
    current_user = session.get('current_user')
    bytes_sum = {}
    user = db.query(SQ_User).filter(SQ_User.login==current_user).first()
    today = date.today()
    begin_of_month = date(year=today.year, month=today.month, day=1)
    bytes_sum['all'] = db.query(func.sum(SQ_Access_Log_Data.bytes))\
                        .filter(SQ_Access_Log_Data.user_name==user.login)\
                        .scalar()
                        
    bytes_sum['month'] = db.query(func.sum(SQ_Access_Log_Data.bytes))\
                        .filter(SQ_Access_Log_Data.user_name==user.login)\
                        .filter(SQ_Access_Log_Data.access_time>=begin_of_month)\
                        .scalar()
                        
    bytes_sum['today'] = db.query(func.sum(SQ_Access_Log_Data.bytes))\
                        .filter(SQ_Access_Log_Data.user_name==user.login)\
                        .filter(SQ_Access_Log_Data.access_time>=today)\
                        .scalar()
    return render_template('user/show_user.html', user=user, bytes_sum=bytes_sum)
    