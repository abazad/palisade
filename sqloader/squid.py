'''
Created on 31.07.2013

@author: bova
'''
from os.path import getsize

class AccessLogParser(object):
    def __init__(self, conf):
        self.conf = conf       
        
    def bytes_to_seek(self):
        file_size = getsize(self.conf.access_log)
        if file_size < self.conf.bytes_to_seek:
            bytes_to_seek = 0
        else:
            bytes_to_seek = self.conf.bytes_to_seek
        return bytes_to_seek
        
    
    def prepare_file(self):
        bytes_to_seek = self.bytes_to_seek()
        self.fh = open(self.conf.access_log, 'r')
        self.fh.seek(bytes_to_seek)
        
    def process_record(self, line):
        record = AccessLogRow(line)
        
    def parse(self):        
        lines = self.fh.readlines(self.conf.buffer)
        if not lines:
            return False
        for line in lines:
            self.process_record(line)
        return True        
        
        
    def write_output(self):
        pass
    
    def load_new_records(self):
        while  self.parse():
            self.write_output()

    def save_state(self):
        bytes_to_seek=self.fh.tell()
        
    def run(self):
        self.prepare_file()
        self.load_new_records()
        self.save_state()
        
        
        


class AccessLogRow(object):
    def __init__(self, line):
        pass
    def get_transformed_line(self):
        pass
