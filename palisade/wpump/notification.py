'''
Created on 02.04.2013

@author: bova
'''

import smtplib
from email.mime.text import MIMEText
import types
import logging

SMTP_HOST = 'zimbra.fido.uz'
SMTP_PORT = '25'
SMTP_USER = 'download@fido.uz'
SMTP_PSWD = 'Q1w3tre'


class Mail(object):
    def __init__(self):
        super(Mail, self).__init__()
        self.serv = None
        self.msg = None                    
    
    def connect(self):
        self.serv = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        self.serv.set_debuglevel(1)
         
    def make_msg(self, rcpt, subj, text):
        self.msg = MIMEText(text)
        self.msg['Subject'] = subj
        self.msg['From'] = SMTP_USER
        self.msg['To'] = ','.join(rcpt)
    
    def disconnect(self):
        self.serv.quit()
        
    def send(self, rcpt, subj, text):
        self.connect()        
        self.make_msg(rcpt, subj, text)
        logging.debug('Try send mail to recepients: %s' % ','.join(rcpt))
        self.serv.sendmail(SMTP_USER, rcpt, self.msg.as_string())
        self.disconnect()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(threadName)-12s %(levelname)-8s %(message)s')
    mailer = Mail()
    mailer.send(['vladimir@fido.uz', 'download@fido.uz'], 'Test WPUMP', 'It is works')
        
        
        
        
    
    
    


