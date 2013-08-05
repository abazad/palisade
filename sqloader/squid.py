'''
Created on 31.07.2013

@author: bova
'''
from os.path import getsize
from urlparse import urlparse

class AccessLogParser(object):
    def __init__(self, conf):
        self.conf = conf
        self.records = []  
        self.output = 'c:/tmp/sq_output.txt'     
        
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
        self.records.append(record)
        
    def parse(self):        
        lines = self.fh.readlines(self.conf.buffer)
        if not lines:
            return False
        for line in lines:
            self.process_record(line)
        return True        
        
        
    def write_output(self):
        with open(self.output, 'a+') as fh:
            for record in self.records:
                fh.write('%s %s\n' % (record.url, record.url_hostname))
    
    def clear_records_list(self):
        del self.records[:]
        
    def load_new_records(self):
        while  self.parse():
            self.write_output()
            self.clear_records_list()

    def save_state(self):
        bytes_to_seek=self.fh.tell()
        self.conf.set_bytes_to_seek(bytes_to_seek)
        print 'Bytes_to_seek: %s' % bytes_to_seek
        
    def run(self):
        self.prepare_file()
        self.load_new_records()
        self.save_state()


class AccessLogRow(object):
    '''Parse squid acces_log record to object's variables
    Example:
        1375177049.785    869 10.50.50.20 TCP_MISS/200 8031 GET bova DIRECT 213.180.204.3 text/html http://ya.ru/
    logformat options from squid:
        logformat palisade %ts.%03tu %6tr %>a %Ss/%03>Hs %<st %rm %un %Sh %<A %mt %45ru
    '''
    def __init__(self, line):
        self.tokens = line.split()
        self.parse()
    
    def parse_request_status(self, token):
        try:
            sq_req_status, http_status_code = token.split('/')
        except:
            sq_req_status = '-'
            http_status_code = '000'
        return sq_req_status, http_status_code
    
    def parse_mime_type(self, token):
        try:
            mime_type, mime_type_desc = token.split('/')
        except:
            mime_type = ''
            mime_type_desc = ''
        return mime_type, mime_type_desc
    
    def get_url_hostname(self):
        r = urlparse(self.url)
        hostname = r.hostname
        if hostname:
            return hostname
        else:
            return self.url
            
        
    def parse(self):
        self.acc_date = self.tokens[0]
        self.response_time = self.tokens[1]
        self.src_ip = self.tokens[2]
        self.sq_req_status, self.http_status_code = self.parse_request_status(self.tokens[3])
        self.bytes = self.tokens[4]
        self.method = self.tokens[5]
        self.username = self.tokens[6]
        self.sq_hierarchy_status=self.tokens[7]
        self.server_fqdn = self.tokens[8]
        self.mime_type, self.mime_type_desc = self.parse_mime_type(self.tokens[9])
        self.url = self.tokens[10]
        self.url_hostname = self.get_url_hostname()
        
    def get_transformed_line(self):
        pass

if __name__ == '__main__':
    r = AccessLogRow("1375177049.785    869 10.50.50.20 TCP_MISS/200 8031 GET bova DIRECT 213.180.204.3 text/html http://ya.ru/")
    r2 = AccessLogRow("1375177049.785    869 10.50.50.20 TCP_MISS/200 8031 GET bova DIRECT 213.180.204.3 text/html 217.69.138.105:443")
    print 'acc_date: %s' % r.acc_date
    print 'response_time: %s' % r.response_time
    print 'src_ip: %s' % r.src_ip
    print 'sq_req_status: %s' % r.sq_req_status
    print 'http_status_code: %s' % r.http_status_code
    print 'bytes: %s' % r.bytes
    print 'method: %s' % r.method
    print 'username: %s' % r.username
    print 'sq_hierarchy_status: %s' % r.sq_hierarchy_status
    print 'server_fqdn: %s' % r.server_fqdn
    print 'mime_type/mime_type_desc: %s/%s' % (r.mime_type, r.mime_type_desc)
    print 'url: %s' % r.url
    print 'url_hostname: %s' %r.url_hostname
    
    print 'r2.url_hostname: %s' % r2.url_hostname
    
    from conf import AppConf
    conf = AppConf('c:/tmp/palisade.conf')
    parser = AccessLogParser(conf)
    parser.run()
        