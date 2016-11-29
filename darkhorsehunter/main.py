# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 17:21:14 2016

@author: smith
"""

import MySQLdb
import sqlalchemy
import datetime as dt
import util.env as env
import monitor as monitor
import analysis as analysis


if __name__ == '__main__':
    conn = MySQLdb.connect(host=env.host, user=env.user, passwd=env.passwd, db=env.db, charset='utf8')
    engine = sqlalchemy.create_engine('mysql://' + env.user + ':' + env.passwd + '@' + env.host + '/' + env.db + '?charset=utf8')

    print 'Scan big deal start: ', dt.datetime.now()
    monitor.monitor(conn)
    print 'Scan big deal end: ', dt.datetime.now()

    print 'Analysis start: ', dt.datetime.now()
    analysis.analysis(conn, engine)
    print 'Analysis end: ', dt.datetime.now()

    conn.close()
    engine.connect().close()




