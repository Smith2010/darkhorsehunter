# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 21:49:18 2016

@author: claude
"""

import tushare as ts
import datetime as dt
import time
import MySQLdb
import main.data.config as cfg
import main.util.common as common
import main.util.dbtools as db


def monitor(connection, data_frame, total_num):
    stock_codes = data_frame['code'].values

    for idx in xrange(0, min(stock_codes.size, total_num)):
        stock_code = stock_codes[idx]

        try:
            real_data = ts.get_realtime_quotes(stock_code)  # Single stock symbol
        except:
            print("Error: ", stock_code)
            continue

        # for i in range(0, 5):  # buy
        #     amount = common.get_value(real_data[cfg.REALTIME_BID_BUY_LIST[2 * i]][0]) * common.get_value(
        #         real_data[cfg.REALTIME_BID_BUY_LIST[2 * i + 1]][0])
        #     if amount * 100 >= cfg.MONITOR_THRESHOLD_AMOUNT:
        #         try:
        #             save_pressure_data(connection, real_data)
        #         except:
        #             continue
        #         break

        for i in range(0, 5):  # sell
            amount = common.get_value(real_data[cfg.REALTIME_BID_SELL_LIST[2 * i]][0]) * common.get_value(
                real_data[cfg.REALTIME_BID_SELL_LIST[2 * i + 1]][0])
            if amount * 100 >= cfg.MONITOR_THRESHOLD_AMOUNT:
                try:
                    save_pressure_data(connection, real_data)
                    print 'sell pressure deal: ', stock_code
                except:
                    continue
                break


def save_pressure_data(connection, real_data):
    raw_data = real_data[cfg.RECORD_FORMAT].values
    date_time = common.get_format_datetime(raw_data[0][-2], raw_data[0][-1])
    data_list = list(raw_data[0][:-2])
    data_list.append(date_time)
    data_tuple = tuple(data_list)
    db.add_pressure_monitor_data(connection, data_tuple)


conn = MySQLdb.connect(host=cfg.host, user=cfg.user, passwd=cfg.passwd, db=cfg.db, charset='utf8')
df = db.get_db_value(conn, 'select * from stock_pool')

while (1):
    print 'Scan big deal start: ', dt.datetime.now()

    monitor(conn, df, cfg.MAX_MONITOR_STOCK_NUM)

    print 'Scan big deal end: ', dt.datetime.now()

    time.sleep(60)
