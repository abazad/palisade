'''
Created on 04.03.2013

@author: bova
'''

import os
import requests
from requests.auth import HTTPProxyAuth

class Wget(object):
    def __init__(self, url):
        self.url = url
        
    def download(self):
        pass
    
    def run(self):
        self.download()


if __name__ == '__main__':
    proxies = {"http": "http://10.50.50.254:3128",
               "https": "http://10.50.50.254:3128"}
    auth = HTTPProxyAuth('admin', 'Q1w3tre123')
    
    r = requests.get('http://megasoft.uz/get/4400?1362552145', proxies=proxies, auth=auth, stream=True)
#    r = requests.get('http://wiki.fido.uz/oracle/book/prog/Scot_Urman_Oracle9i.pdf', stream=True)
    print r.url
    file_name = os.path.basename(r.url)
    file_size = float(r.headers['content-length'])    
    chunk_size = 1024000
    downloaded_size = 0
        
    with open(os.path.join('c:/tmp/',file_name),'wb') as fh:
        for data in r.iter_content(chunk_size):
            fh.write(data)
            downloaded_size += chunk_size
            downloaded_pct = round(downloaded_size/file_size*100)
            print "already downloaded: %s" % downloaded_pct
            
        