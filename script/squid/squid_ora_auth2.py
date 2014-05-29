#!/usr/bin/python

import sys
import time
import logging
import os

os.environ['ORACLE_HOME'] = '/u01/app/oracle/instantclient_11_2'
os.environ['LD_LIBRARY_PATH'] = os.environ['ORACLE_HOME']

import cx_Oracle

#engine = create_engine("oracle://hr:Q1w3tre321@10.50.50.122:1521/fbs", echo=False)


if __name__ == '__main__':
    logging.basicConfig(filename='/tmp/squid_ora_auth.log',level=logging.DEBUG)
    logging.debug('Starting auth helper loop with pid: %s' % os.getpid())
    while True:
        try:
            conn = cx_Oracle.connect('palisade/Q1w3tre321@10.50.50.123/palisade')
            cursor = conn.cursor()
        except:
            logging.debug('DB Connection error: %s' % sys.exc_info()[0])
            result = "ERR database error"

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
            cursor.execute('''select login, password from SQ_USER where login=:login and status=:status''', login=login, status='A')
            user = cursor.fetchone()
            conn.close()
        except:
            logging.debug('Unexpected error: %s' % sys.exc_info()[0])
            result = "ERR database error"
        else:
            if user and user[1] == password:
                result = "OK"
            else:
                result = "ERR password not match"

        logging.debug('Line to stdout: %s; Worker PID is: %s' % (result, os.getpid()))
        sys.stdout.write("%s\n" % result)
        sys.stdout.flush()
#Reset variables
        login = ''
        password = ''
        result = ''
logging.debug('Exiting auth helper loop with pid: %s' % os.getpid())
