# -*- coding: utf8 -*-
'''
Created on 15.04.2013

@author: bova
'''
from flask import render_template, request, redirect, url_for, flash, g, session, jsonify
from palisade.ui.wpump import wpump
from palisade.db.schema import WPDownload, SQ_User
from palisade.db.conn import Session

from datetime import date, datetime

from palisade.ui.decorators import login_required, admin_required
from palisade.ui.wpump.form import DownloadForm
from palisade.wpump.wget_thread import State as WPState


@wpump.route('/')
def index():
    conn = Session()
    if request.method == 'GET':
        offset = request.args.get('iDisplayStart', 0,   type=int)
        limit = request.args.get('iDisplayLength', 10, type=int)
        echo = request.args.get('sEcho', type=int)        
        count = conn.query(WPDownload).count()
        current_user = session.get('current_user')
        user = conn.query(SQ_User).filter(SQ_User.login==current_user).first()
        downloads = conn.query(WPDownload).\
                    filter(WPDownload.owner_id==user.id).\
                    all()[offset:offset+limit]        
    return render_template('wpump/index.html', downloads=downloads)
       

@wpump.route('/download', methods=['GET', 'POST'])
def download():
    conn = Session()    
    form = DownloadForm(request.form)    
    if request.method == 'POST' and form.validate():
        current_user = session.get('current_user')
        user = conn.query(SQ_User).filter(SQ_User.login==current_user).first()
        conn.add(WPDownload(form.url.data, user.id, datetime.now()))#TODO: fix user.id
        conn.commit()
        return redirect(url_for('wpump.index'))
    return render_template('wpump/form/download.html', form=form)

@wpump.route('/dispatch/<int:download_id>', methods=['GET', 'POST'])
def dispatch(download_id):
    conn = Session()
    download = conn.query(WPDownload).filter_by(id=download_id).one()    
    if request.method == 'GET':
        if request.args['action'] == 'accept':
            download.state_id = WPState.accepted
        elif request.args['action'] == 'reject':
            download.state_id = WPState.rejected
        elif request.args['action'] == 'delete':
            conn.delete(download)
    conn.commit()
    return redirect(url_for('wpump.admin'))

@wpump.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    conn = Session()
    if request.method == 'GET':
        offset = request.args.get('iDisplayStart', 0,   type=int)
        limit = request.args.get('iDisplayLength', 100, type=int)
        echo = request.args.get('sEcho', type=int)
        
        count = conn.query(WPDownload).count()
        downloads = conn.query(WPDownload).all()[offset:offset+limit]
    return render_template('wpump/admin.html', downloads=downloads)

@wpump.route('/download_edit', methods=['GET', 'POST'])
def download_edit():
    return render_template('wpump/edit.html', download_id=request.args.id)

@wpump.route('/_download_admin')
def _download_admin():
    conn = Session()
    if request.method == 'GET':
        offset = request.args.get('iDisplayStart', 0,   type=int)
        limit = request.args.get('iDisplayLength', 10, type=int)
        echo = request.args.get('sEcho', type=int)
        
        count = conn.query(WPDownload).count()
        tasks = conn.query(WPDownload).all()[offset:offset+limit]
        aaData = [[t.id, t.url, t.email, t.state, '0'] for t in tasks]
        return jsonify(sEcho=echo+1, iTotalRecords=count, 
                       iTotalDisplayRecords=count, 
                       aaData=aaData)
       
