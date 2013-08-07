import sys
import os

from conf import AppConf
from squid import AccessLogParser
from transport import FTPTransport
import logging

        
APP_VERSION = '1.0'

def main():
    try:
        conf_file = sys.argv[1]
    except:
        print "Usage:", sys.argv[0], "conf_file_path"
        sys.exit(1)
    else:
        loader = SQLoader(conf_file)
        loader.run()


class SQLoader(object):
    def __init__(self, conf_file):
        self.conf = AppConf(conf_file)
        logging.basicConfig(filename=self.conf.log_file, level=logging.DEBUG)
        self.parser = AccessLogParser(self.conf)
        self.transporter = FTPTransport()
    
    def run(self):
        self.parser.run()
        self.transporter.copy(self.parser.output_path)


if __name__ == '__main__':
    main()    
        
    

