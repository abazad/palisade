# -*- coding: utf8 -*-
'''
Created on 04.03.2013

@author: bova
'''

import os
import requests
from requests.auth import HTTPProxyAuth
import threading
import logging
import database as db
import time
from structure import Downloads, EmptyQueueError, FINISHED, STARTED, download_state
from Tkinter import *
from notification import Mail
import os
from xmpp_send import SendMsgBot

THREAD_COUNT = 3
IS_RUNNING = True
OUTPUT_DIR='X:\download'


            
class WgetState:
    IS_RUNNING = True

class WgetWorker(threading.Thread):
    '''Download specified url    
    '''
    def __init__(self, s, downloads):
        threading.Thread.__init__(self)        
        self.s = s
        self.downloads = downloads      
        self.my_name = ''  
           
    def pump(self):
#        r = requests.get('http://megasoft.uz/get/4400?1362552145', proxies=proxies, auth=auth, stream=True)        
#TODO: Ignore ssl cert error
#SSLError: [Errno 1] _ssl.c:490: error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed
        r = requests.get(self.task.url, stream=True)
        file_name = os.path.basename(r.url)
        try:
            file_size = float(r.headers['content-length'])
        except:
            logging.debug("File Size unknown")
            logging.error('%s' % sys.exc_info()[0])
            file_size = float(1024000000)        
        logging.debug('Start downloading: \
URL: %s \
File Name: %s \
File Size: %s' % (self.task.url, file_name, file_size))  
        chunk_size = 1024000
        downloaded_size = 0        
            
        with open(os.path.join(OUTPUT_DIR,file_name),'wb') as fh:
            for data in r.iter_content(chunk_size):
                if IS_RUNNING == False:
                    break
                fh.write(data)
                downloaded_size += chunk_size
                downloaded_pct = round(downloaded_size/file_size*100)
                logging.debug('[%s] %s%%' % (file_name, downloaded_pct))

        
    def do_work(self):
        logging.debug('Try to acquire download queue...')
        with self.s:
            logging.debug('Queue acquired')
            self.downloads.update_task_attr(self.task.id, 'worker', self.my_name)
            self.pump()
            self.downloads.update_task_attr(self.task.id, 'state', download_state['completed'])
            
    def run(self):
        self.my_name = threading.currentThread().getName()        
        while WgetState.IS_RUNNING:
            logging.debug('WgetWorker.run IS_RUNNING=%s' % str(WgetState.IS_RUNNING))
            try:
                self.task = self.downloads.get_url(self.my_name)
            except EmptyQueueError:
                pass                
            else:
                self.do_work()
            finally:
                time.sleep(2)

class WgetDB(threading.Thread):
    def __init__(self, downloads):
        threading.Thread.__init__(self)
        self.downloads = downloads      
        self.conn = db.Session()  
    
    def get_new(self):
        rows = self.conn.query(db.WpumpTask).filter_by(state=download_state['accepted'])
#            self.db.cursor.execute('select * from wpump_task where state=?', 'N')
        for row in rows:                            
            logging.debug('New URL found in database %s' % row.url)
            self.downloads.put(row)
            row.state = download_state['active']
#            self.db.cursor.execute("""update wpump_task set state='Started' where state='N'""")
        self.conn.commit()
    
    def update_statistic(self):
        pass
            
    def run(self):
        while WgetState.IS_RUNNING:
            self.get_new() 
            time.sleep(2)

class WgetNotif(threading.Thread):
    def __init__(self, downloads):
        threading.Thread.__init__(self)
        self.downloads = downloads
#        self.mailer = Mail()
        self.xmpp = SendMsgBot()
        self.conn = db.Session()
    
    def do_work(self, rcpt=None):
        send_to = rcpt and rcpt or self.task.email
        new_url = '\\\\nserver\in_out\download\%s' % os.path.basename(self.task.url)
#        self.mailer.send([self.task.email], 'WgetNotif', new_url)
        self.xmpp.chat(send_to, new_url)
    
    def notify_admin(self):
        admin_xmpp_id = u'vladimir@fido.uz'
        rows = self.conn.query(db.WpumpTask).filter_by(state=download_state['new'])
#            self.db.cursor.execute('select * from wpump_task where state=?', 'N')
        for row in rows:                            
            logging.debug('New URL found in database %s' % row.url)
            self.xmpp.chat(admin_xmpp_id, row.url)            
            row.state = download_state['new1']
#            self.db.cursor.execute("""update wpump_task set state='Started' where state='N'""")
        self.conn.commit()
        time.sleep(3)
        
    
    def notify_client(self):
        try:
            self.task = self.downloads.get_completed()
        except EmptyQueueError:                
            pass
        else:
            self.do_work()
        finally:
            time.sleep(3)

    
    def run(self):
        while WgetState.IS_RUNNING:
            self.notify_admin()
            self.notify_client()
                            
                
    
class WgetManager(object):
    def __init__(self):        
        self.s = threading.Semaphore(2)
        self.l = threading.Lock()
        self.downloads = Downloads()
        self.threads = []
    
    def init_workers(self):
        for i in range(THREAD_COUNT):
            t = WgetWorker(self.s, self.downloads)
            self.threads.append(t)
            t.start()
    
    def init_db(self):
        t = WgetDB(self.downloads)
        self.threads.append(t)
        t.start()
    
    def init_notification(self):
        t = WgetNotif(self.downloads)
        self.threads.append(t)
        t.start()
        
    def run(self):
        self.init_workers()
        self.init_db()
        self.init_notification()
    
    def stop(self):
        logging.debug('WgetManager.stop')
        self.l.acquire()        
        WgetState.IS_RUNNING = False
        self.l.release()
        logging.debug('WgetManager.stop IS_RUNNING=%s' % str(WgetState.IS_RUNNING))
        for t in self.threads:
            t.join()
    


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(threadName)-12s %(levelname)-8s %(message)s')

    proxies = {"http": "http://10.50.50.254:3128",
               "https": "http://10.50.50.254:3128"}
    auth = HTTPProxyAuth('admin', 'Q1w3tre123')
    
    urls = ['http://10.50.50.254/FAR.7z', 
            'http://10.50.50.254/database_nt.rar', 
            'http://10.50.50.254/FAR.rar',
            'http://10.50.50.254/openvpn-2.2.2-install.exe']
    
    workers = []

wget_manager = WgetManager()
wget_manager.run()
time.sleep(3)

#UI
ui_root = Tk()
ui_frame = Frame(ui_root)
ui_frame.pack()
ui_btn = Button(ui_frame)
ui_btn['text'] = 'Stop'
ui_btn['command'] = wget_manager.stop
ui_btn.pack()
ui_root.mainloop()
#    s = threading.Semaphore(2)
#    for url in urls:
#        t = WgetWorker(url, s)
#        workers.append(t)
#        t.start()
#    
#    for t in workers:
#        t.join()
        
#    r = requests.get('http://wiki.fido.uz/oracle/book/prog/Scot_Urman_Oracle9i.pdf', stream=True)
            
        