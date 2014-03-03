# -*- coding: utf8 -*-
'''
Created on 04.03.2013

@author: bova
'''

import os
import sys
import requests
from requests.auth import HTTPProxyAuth
import threading
import logging
import time
from structure import Downloads, EmptyQueueError, FINISHED, STARTED, download_state
#from Tkinter import *
from notification import Mail
from xmpp_send import SendMsgBot
from palisade.db.conn import Session
from palisade.db.schema import WPDownload
from palisade.conf import PalisadeConfig

conf = PalisadeConfig()

THREAD_COUNT = conf.wpump.thread_count
OUTPUT_DIR=conf.wpump.output_dir
CHUNK_SIZE = conf.wpump.chunk_size

IS_RUNNING = True
ADMIN_XMPP_ID = u'vladimir@fido.uz'

class State(object):
    new = 1
    accepted = 2
    scheduled = 3
    active = 4
    pause = 5
    success = 6
    failure = 7
    new1 = 11#TODO: need improve notification module 
    rejected = 12
    finished = [success, failure, rejected]

            
class WgetState:
    IS_RUNNING = True

class WgetWorker(threading.Thread):
    '''Download specified url    
    '''
    def __init__(self, s):
        threading.Thread.__init__(self)        
        self.s = s          
        self.my_name = ''
        self.download = None

    def log(self):        
        downloaded_pct = round(self.download.bytes_completed/self.download.bytes*100)
        logging.info('[%s] %s%%' % (self.file_name, downloaded_pct))

    def get_file_size(self):
        try:
            self.download.bytes = float(self.r.headers['content-length'])
            self.conn.commit()
        except:
            logging.error("File Size unknown",exc_info=True)
            self.download.bytes = float(1024000000)
                       
    def pump(self):   
        self.r = requests.get(self.download.url, stream=True)
        self.file_name = os.path.basename(self.r.url)     
        self.get_file_size()            
        
        logging.info('Start downloading:\n URL: %s \n File Name: %s \n File Size: %s' \
                      % (self.download.url, self.file_name, self.download.bytes))  
            
        with open(os.path.join(OUTPUT_DIR, self.file_name),'wb') as fh:
            for data in self.r.iter_content(CHUNK_SIZE):
                if IS_RUNNING == False:
                    break
                fh.write(data)
                self.download.bytes_completed += CHUNK_SIZE
                self.conn.commit()
        

    def execute(self):
        logging.debug('Try to acquire download queue...')
        with self.s:
            logging.debug('Queue acquired')
            self.download.state_id = State.active
            self.conn.commit()
            try:
                self.pump()
            except:
                self.download.state_id = State.failure
                print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
Error occured while pupm() proc: %s' % sys.exc_info()[2]
            else:
                self.download.state_id = State.success
            finally:
                self.conn.commit()
                self.conn.close()
            
    def run(self):
        self.my_name = threading.currentThread().getName()        
        while WgetState.IS_RUNNING:
            self.download = None
            self.conn = Session()
            logging.debug('WgetWorker.run IS_RUNNING=%s' % 'WOrker')
            self.download = self.conn.query(WPDownload).\
                            filter(WPDownload.state_id==State.accepted).\
                            with_lockmode('update').\
                            first()   
            if self.download:
                self.execute()                            
            else:
                self.conn.commit() 
                self.conn.close()               
                time.sleep(2)            
            


class WgetNotif(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)        
        self.download = None
        self.mailer = Mail()
        self.xmpp = SendMsgBot()        
   
    def notify_admin(self):
        downloads = self.conn.query(WPDownload).\
                        filter(WPDownload.state_id==State.new)

        for download in downloads:                            
            logging.info('New URL found in database %s' % download.url)
            self.xmpp.chat(ADMIN_XMPP_ID, download.url)            
            download.state_id = State.new1
#            self.db.cursor.execute("""update wpump_task set state_id='Started' where state_id='N'""")
        self.conn.commit()    

    def notify_client_helper(self, download):
        send_to = download.owner.email
        new_url = '\\\\nserver\in_out\download\%s' % os.path.basename(download.url)
        self.mailer.send(send_to, 'Palisade.WPUMP.Notif', new_url)
#        self.xmpp.chat(send_to, new_url)
    
    def notify_client(self):
        downloads = self.conn.query(WPDownload).\
                    filter(WPDownload.is_notified==False).\
                    filter(WPDownload.state_id.in_(State.finished))
        for download in downloads:
            try:
                self.notify_client_helper(download)
            except:
                print 'JOPAAAA ERROR %s' % sys.exc_info()[0]
            else:
                download.is_notified = True
        self.conn.commit()        
    
    def run(self):
        while WgetState.IS_RUNNING:
            self.conn = Session()
            self.notify_admin()
            self.notify_client()
            self.conn.close()
            time.sleep(3)    
                            
                
    
class WgetManager(object):
    def __init__(self):        
        self.s = threading.Semaphore(2)
        self.l = threading.Lock()        
        self.threads = []
    
    def init_workers(self):
        for i in range(THREAD_COUNT):
            t = WgetWorker(self.s)
            self.threads.append(t)
            t.start()
   
        
    def init_notification(self):
        t = WgetNotif()
        self.threads.append(t)
        t.start()
        
    def run(self):
        self.init_workers()
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
        
#    #UI
#    ui_root = Tk()
#    ui_frame = Frame(ui_root)
#    ui_frame.pack()
#    ui_btn = Button(ui_frame)
#    ui_btn['text'] = 'Stop'
#    ui_btn['command'] = wget_manager.stop
#    ui_btn.pack()
#    ui_root.mainloop()
    #    s = threading.Semaphore(2)
    #    for url in urls:
    #        t = WgetWorker(url, s)
    #        workers.append(t)
    #        t.start()
    #    
    #    for t in workers:
    #        t.join()
            
    #    r = requests.get('http://wiki.fido.uz/oracle/book/prog/Scot_Urman_Oracle9i.pdf', stream=True)
                
            