import sys
import os

from conf import AppConf
from squid import AccessLog
        


def main():
    try:
        conf_file = sys.argv[1]
    except:
        print "Usage:", sys.argv[0], "conf_file_path"
        sys.exit(1)
    
    conf = AppConf(conf_file)
    
    print conf.last_loaded_line


class SQLoader(object):
    def __init__(self, conf):
        self.conf = conf


if __name__ == '__main__':
    main()    
        
    

