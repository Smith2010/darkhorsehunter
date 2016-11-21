# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 21:49:18 2016

@author: claude
"""
from main.utiliy.dbUtil import *
from main.utiliy.NormalUtil import *
from config import *
import tushare as ts
import time
import datetime
import MySQLdb


'''
# no longer need
def GetStocksToBeObserved():
    raw_data_df = ts.get_stock_basics()
    stock_idx = raw_data_df.filter(raw_data_df.outstanding < THRESH_HOLD_OUTSTANDING)
    return stock_idx.index.values
'''

def GetWatchList(stock_codes, total_num):
    watch_list = []
    for idx in xrange(0, min(stock_codes.size, total_num)):
        stock_code = stock_codes[idx]
        df = ts.get_realtime_quotes(stock_code)  # Single stock symbol
        df[REALTIME_BASIC_LIST + REALTIME_BID_BUY_LIST + REALTIME_BID_SELL_LIST]
        #        for i in range(0,5):#buy
        #            amount = GetValue(df[REALTIME_BID_BUY_LIST[2*i]][0])*GetValue(df[REALTIME_BID_BUY_LIST[2*i+1]][0])
        #            if amount>=THRESH_MOUNT:
        #                watch_list.append(stock_code)
        #                break
        for i in range(0, 5):  # sell
            amount = GetValue(df[REALTIME_BID_SELL_LIST[2 * i]][0]) * GetValue(df[REALTIME_BID_SELL_LIST[2 * i + 1]][0])
            if amount >= THRESH_AMOUNT:
                watch_list.append(stock_code)
                break
    return watch_list


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


def Monitor(conn, df, total_num):
    cnt = 3
    while cnt > 0:
        # print "Monitor", df['code'].values
        watch_list = GetWatchList(df['code'].values, total_num)
        # print watch_list
        time.sleep(3)
        for code in watch_list:
            try:
                this_df = ts.get_realtime_quotes(code)
            except:
                continue
            raw_data = this_df[RECORD_FORMAT].values
            date_time = GetFormatdatetime(raw_data[0][-2], raw_data[0][-1])
            data_list = list(raw_data[0][:-2])
            data_list.append(date_time)
            data_tuple = tuple(data_list)
            # print data_tuple
            try:
                InsertDbPrssMoni(conn, data_tuple)
            except:
                pass
        cnt -= 1


if __name__ == "__main__":
    conn = MySQLdb.connect(host="106.14.42.175", user="duser", passwd="1qaz@WSX", db="darkhorse", charset="utf8")
    sql = "select * from stock_pool"
    df = GetDbValue(conn, sql)
    ###
    data = (
    '600001', '测试', '1.11', '100', '1.12', '99', '1.13', '99999', '1.14', '7', '1.15', '8', '1.10', '99999', '1.09',
    '9', '1.08', '9', '1.07', '9', '1.06', '9', '20161119101112')
    InsertDbPrssMoni(conn, data)
    conn.close();