'''
Created on Jul 16, 2013

@author: bova
'''
from flask import render_template, request, redirect, url_for, flash
from palisade.ui.admin import admin
from palisade.db.schema import SQ_User, SQ_Report_Data
from palisade.db.conn import Session
from palisade.ui.forms import UserForm

from palisade.ui.decorators import login_required, admin_required

#@admin.route('/', defaults={'page': 'index'})
@admin.route('/user')
@login_required
@admin_required
def show_users():
    session = Session()
    users = session.query(SQ_User).all()
            
    return render_template('admin/show_users.html', users=users)

@admin.route('/user/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = SQ_User(form.first_name.data,
                       form.last_name.data,
                       form.login.data,
                       form.password.data,
                       form.email.data,
                       form.is_admin.data,                       
                       'A',
                       form.traffic_limit.data)
        session = Session()
        session.add(user)
        session.commit()
        flash("User successfully added!")
        session.close()
        return redirect(url_for('.show_users'))    
    return render_template('admin/add_user.html', form=form)

#TODO: add feedback after form validate
@admin.route('/user/edit/<user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id=None):
    session=Session()
    user = session.query(SQ_User).filter(SQ_User.id==user_id).first()
    form = UserForm(request.form, user)
    if request.method == 'POST' and form.validate:
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.traffic_limit = form.traffic_limit.data
        session.commit()      
        session.close()  
        return redirect(url_for('.show_users'))
    return render_template('admin/edit_user.html', form=form)

@admin.route('/user/delete/<user_id>', methods=['GET'])
@login_required
@admin_required
def delete_user(user_id):
    session = Session()
    user = session.query(SQ_User).filter(SQ_User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
        session.close()
        flash("User successfully deleted.")
    else:
        flash("User doesn't exist")    
    return redirect(url_for('.show_users'))

@admin.route('/report', methods=['GET'])
def report_index():
    return render_template('admin/report_index.html')

@admin.route('/report/get/<report_id>', methods=['GET', 'POST'])
def get_report(report_id):
    session = Session()
    reports = session.query(SQ_Report_Data).\
                filter(SQ_Report_Data.report_name==report_id).\
                all()
    session.close()
    return render_template('admin/get_report.html', reports=reports, report_name=report_id)

@admin.route('/report/make/<report_id>', methods=['GET', 'POST'])
def make_report(report_id):
    session = Session()
    session.execute("begin sq_reports.run_report('%s');end;" % report_id)
    session.close()
    return redirect(url_for('.get_report', report_id=report_id))

@admin.route('/report/show/<report_id>', methods=['GET'])
def show_report(report_id):
    session = Session()
    report = session.query(SQ_Report_Data).filter(SQ_Report_Data.id==report_id).one()
    session.close()
    return render_template('admin/show_report.html', report=report)
    

    
    