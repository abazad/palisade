'''
Created on 31.07.2013

@author: bova
'''
import ConfigParser
import os.path


class AppConf(object):
    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.conf = ConfigParser.ConfigParser()
        self.load_conf()            
    
    def save_config(self):
        with open(self.conf_file, 'w') as fh:
            self.conf.write(fh)
            
    def load_default(self):
        self.conf.add_section('general')
        self.conf.add_section('runtime')
        self.conf.set('general', 'buffer', '1000')
        self.conf.set('general', 'log_file', '/var/log/palisade/sqloader.log')
        self.conf.set('general', 'access_log', '/var/log/squid3/palisade.log')
        self.conf.set('general', 'output_dir', '/tmp')
        self.conf.set('runtime', 'bytes_to_seek', '0')        
        self.save_config()
    
    def read_conf(self):
        self.conf.read(self.conf_file)
        
    def populate_variables(self):
        self.buffer = self.conf.getint('general', 'buffer')
        self.log_file = self.conf.get('general', 'log_file')
        self.access_log = self.conf.get('general', 'access_log')
        self.output_dir = self.conf.get('general', 'output_dir')
        self.bytes_to_seek = self.conf.getint('runtime', 'bytes_to_seek')
        
    def load_conf(self):
        if os.path.exists(self.conf_file):
            self.load_conf()
        else:
            self.load_default()
        
        self.populate_variables()        