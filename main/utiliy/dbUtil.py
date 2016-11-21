# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 16:11:15 2016

@author: oncast
"""

import tushare as ts
import datetime
import MySQLdb
import pandas as pd



def GetDbValue(conn, sql):
    try:
        return pd.read_sql(sql, conn);
    except IOError:
        return None


def InsertDbPrssMoni(conn, MoniStock):
    try:
        cur = conn.cursor()
        sqli = "insert into pressure_monitor values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sqli, MoniStock)
        cur.close()
        conn.commit()
        return 0
    except IOError:
        return None


def GetPressureStockList(conn, date):
    try:
        codes = []
        cur = conn.cursor()
        sql = "select distinct(code)  from pressure_monitor where datatime like  '" + date + "%%'"
        dfs = cur.execute(sql)
        info = cur.fetchmany(dfs)
        for ii in info:
            codes.append(ii[0])
        cur.close()
        return pd.DataFrame({"code": pd.Series(codes)})
    except IOError:
        return None


def GetAnyaysisPressure(conn, date, code):
    try:
        sql = "select * from  pressure_monitor where datatime like  '" + date + "%'" + " and code='" + code + "' order by datatime"
        #        print sql
        return pd.read_sql(sql, conn)
    except IOError:
        return None







# conn = MySQLdb.connect(host="106.14.42.175",user="duser",passwd="1qaz@WSX",db="darkhorse",charset="utf8")


#sql = "select * from stock_pool"

# df = GetDbValue(conn,sql)
# print df
# data=('600002','测试','1.11','100','1.12','99','1.13','99999','1.14','7','1.15','8','1.10','99999','1.09','9','1.08','9','1.07','9','1.06','9','20161119101917')
# InsertDbPrssMoni(conn,data)

# dft=GetPressureStockList(conn,'20161119')
# print dft
# conn.close();

# print GetFormatdatetime("2016-11-19","11:01:12")


# print  datetime.datetime.now().strftime("%Y%m%d%H%M%S")
'''
X_DAYS_AGO=10
DayAgo = (datetime.datetime.now() - datetime.timedelta(days = X_DAYS_AGO))

strdate=DayAgo.strftime("%Y%m%d")

print

if(int(strdate) > int(marketdate)):
    print 'YES'
'''



#    print ts.get_realtime_quotes('000033')