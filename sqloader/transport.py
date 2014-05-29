'''
Created on 07.08.2013

@author: bova
'''

from ftplib import FTP
import os.path


class FTPTransport(object):
    SERVER = '10.50.50.123'
    LOGIN = 'oracle'
    PASSWORD= 'oracle11g'
    REMOTE_DIR = '/u02/export/palisade'

    def __init__(self):
        self.ftp = FTP(self.SERVER)

    def login(self):
        self.ftp.login(self.LOGIN, self.PASSWORD)

    def copy(self, file_path):
        file_name = os.path.basename(file_path)
        self.login()
        self.ftp.cwd(self.REMOTE_DIR)
        with open(file_path, 'rb') as fh:
            self.ftp.storbinary('STOR ' + file_name, fh)
        self.ftp.quit()

if __name__ == '__main__':
    ftp_transport = FTPTransport()
    ftp_transport.copy('c:/tmp/sq_output.txt')

