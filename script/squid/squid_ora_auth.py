#!/usr/bin/python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

import sys
import time
import logging
import os

os.environ['ORACLE_HOME'] = '/u01/app/oracle/instantclient_11_2'
os.environ['LD_LIBRARY_PATH'] = os.environ['ORACLE_HOME']

Base = declarative_base()

engine = create_engine("oracle://hr:Q1w3tre321@10.50.50.122:1521/fbs", echo=False)
Session = sessionmaker(engine)


class SQ_User(Base):
    __tablename__ = 'sq_user'

    id = Column(Integer, Sequence('sq_user_id_seq'), primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    login = Column(String(50))
    password = Column(String(250))
    status = Column(String(3))
    traffic_limit = Column(Integer(9))

    def __init__(self, first_name, last_name, password, status, traffic_limit):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.status = status
        self.traffic_limit = traffic_limit

    def __repr__(self):
        return "<SQ_USER('%s', '%s', '%s', '%s', '%s')>" % (self.first_name, self.last_name, 'secret', self.status, self.traffic_limit)

if __name__ == '__main__':
    logging.basicConfig(filename='/tmp/squid_ora_auth.log',level=logging.DEBUG)    
    while True:
        try:
            line = sys.stdin.readline()
            line = line.strip()
            logging.debug('line from stdin: %s' % line)
        except KeyboardInterrupt:
            break
        try:
            login, password = line.split()
            logging.debug('Login/Password: %s/%s' % (login, password))
        except ValueError:
            result = "ERR split error"        
        
        try:
            session = Session()
            user = session.query(SQ_User).filter(SQ_User.login==login).first()
        except:
            result = "ERR database error"
        else:
            if user and user.password == password:
                result = "OK"
            else:
                result = "ERR password not match"

        logging.debug('Line to stdout: %s' % result)
        sys.stdout.write("%s\n" % result)
        sys.stdout.flush()     


