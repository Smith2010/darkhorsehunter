# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 17:21:14 2016

@author: smith
"""

import MySQLdb
import sqlalchemy
import datetime as dt
import monitor as monitor
import analysis as analysis
import os

host = os.getenv('DARKHORSE_HOST')
user = os.getenv('DARKHORSE_USER')
passwd = os.getenv('DARKHORSE_PASSWD')
db = os.getenv('DARKHORSE_DB')

if __name__ == '__main__':
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset='utf8')
    engine = sqlalchemy.create_engine('mysql://' + user + ':' + passwd + '@' + host + '/' + db + '?charset=utf8')

    print 'Scan big deal start: ', dt.datetime.now()
    monitor.monitor(conn)
    print 'Scan big deal end: ', dt.datetime.now()

    print 'Analysis start: ', dt.datetime.now()
    analysis.analysis(conn, engine)
    print 'Analysis end: ', dt.datetime.now()

    conn.close()
    engine.connect().close()
