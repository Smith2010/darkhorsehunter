# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 21:49:18 2016

@author: claude
"""

import tushare as ts
import util.common as common
import util.dbtools as db

REALTIME_BID_BUY_LIST = ['b1_p', 'b1_v', 'b2_p', 'b2_v', 'b3_p', 'b3_v', 'b4_p', 'b4_v', 'b5_p', 'b5_v']
REALTIME_BID_SELL_LIST = ['a1_p', 'a1_v', 'a2_p', 'a2_v', 'a3_p', 'a3_v', 'a4_p', 'a4_v', 'a5_p', 'a5_v']
RECORD_FORMAT = ['code', 'name'] + REALTIME_BID_SELL_LIST + REALTIME_BID_BUY_LIST + ['date', 'time']
MONITOR_THRESHOLD_AMOUNT = 10000000


def monitor(connection, total_num):
    data_frame = db.get_db_value(connection, 'select * from stock_pool')

    stock_codes = data_frame['code'].values

    for idx in xrange(0, min(stock_codes.size, total_num)):
        stock_code = stock_codes[idx]

        try:
            real_data = ts.get_realtime_quotes(stock_code)  # Single stock symbol
        except Exception as e:
            print(e)
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
            amount = common.get_value(real_data[REALTIME_BID_SELL_LIST[2 * i]][0]) * common.get_value(
                real_data[REALTIME_BID_SELL_LIST[2 * i + 1]][0])
            if amount * 100 >= MONITOR_THRESHOLD_AMOUNT:
                try:
                    save_pressure_data(connection, real_data)
                    print 'sell pressure deal: ', stock_code
                except Exception as e:
                    print(e)
                except:
                    print("Error: ", stock_code)
                    continue
                break


def save_pressure_data(connection, real_data):
    raw_data = real_data[RECORD_FORMAT].values
    date_time = common.get_format_datetime(raw_data[0][-2], raw_data[0][-1])
    data_list = list(raw_data[0][:-2])
    data_list.append(date_time)
    data_tuple = tuple(data_list)
    db.add_pressure_monitor_data(connection, data_tuple)


