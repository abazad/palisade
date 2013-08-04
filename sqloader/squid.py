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
    '''Parse squid acces_log record to object's variables
    Example:
    1375177049.785    869 10.50.50.20 TCP_MISS/200 8031 GET bova DIRECT/213.180.204.3 text/html http://ya.ru/
    
    '''
    def __init__(self, line):
        self.tokens = line.split()
        self.parse()
    
    def parse_state(self, token):
        pass
    
    def parse_mime_type(self, token):
        pass
        
    def parse(self):
        self.acc_date = self.tokens[0]
        self.response_time = self.tokens[1]
        self.src_ip = self.tokens[2]
        self.parse_state(self.tokens[3])
        self.bytes = self.tokens[4]
        self.method = self.tokens[5]
        self.username = self.tokens[6]
        self.acc_method = ''
        self.parse_mime_type(self.tokens[8])
        self.url = self.tokens[9]
        
    def get_transformed_line(self):
        pass

if __name__ == '__main__':
    al_row = AccessLogRow("1375177049.785    869 10.50.50.20 10.50.50.20 TCP_MISS/200 8031 GET bova DIRECT/213.180.204.3 text/html http://ya.ru/")
    print al_row.acc_date, al_row.response_time
    
    