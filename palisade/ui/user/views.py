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

from palisade.ui.decorators import login_required

@user.route('/', methods=['GET'])
@login_required
def show_user():
    db = Session()
    current_user = session.get('current_user')
    bytes_sum = {}
    user = db.query(SQ_User).filter(SQ_User.login==current_user).first()
    today = date.today()
    begin_of_month = date(year=today.year, month=today.month, day=1)
    bytes = db.query(func.sum(SQ_Access_Log_Data.bytes))\
                        .filter(SQ_Access_Log_Data.user_name==user.login)\
                        .scalar()
    bytes_sum['all'] = bytes and bytes or 0
                        
    bytes = db.query(func.sum(SQ_Access_Log_Data.bytes))\
                        .filter(SQ_Access_Log_Data.user_name==user.login)\
                        .filter(SQ_Access_Log_Data.access_time>=begin_of_month)\
                        .scalar()
    bytes_sum['month'] = bytes and bytes or 0
                        
    bytes = db.query(func.sum(SQ_Access_Log_Data.bytes))\
                        .filter(SQ_Access_Log_Data.user_name==user.login)\
                        .filter(SQ_Access_Log_Data.access_time>=today)\
                        .scalar()
    bytes_sum['today'] = bytes and bytes or 0
    return render_template('user/show_user.html', user=user, bytes_sum=bytes_sum)
    