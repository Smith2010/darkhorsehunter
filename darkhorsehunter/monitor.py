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
BATCH_SIZE = 100


def monitor(connection):
    data_frame = db.get_db_value(connection, 'select code from stock_pool')
    stock_codes = data_frame['code'].values

    idx = 0
    while idx * BATCH_SIZE < stock_codes.size:
        start = idx * BATCH_SIZE
        end = (idx + 1) * BATCH_SIZE if (idx + 1) * BATCH_SIZE < stock_codes.size else stock_codes.size
        stock_code = stock_codes[start:end]
        idx += 1

        try:
            real_data = ts.get_realtime_quotes(stock_code.tolist())  # 30 stocks symbol
            for j in range(0, len(real_data.index)):
                # for i in range(0, 5):  # buy
                #     amount = common.get_float_value(
                #         real_data[REALTIME_BID_BUY_LIST[2 * i]][0]) * common.get_float_value(
                #         real_data[REALTIME_BID_BUY_LIST[2 * i + 1]][0])
                #     if amount * 100 >= MONITOR_THRESHOLD_AMOUNT:
                #         real_pressure_data = real_data[j:j + 1]
                #         save_pressure_data(connection, real_pressure_data)
                #         print 'buy pressure deal: ', stock_code[j]
                #         break

                for i in range(0, 5):  # sell
                    amount = common.get_float_value(
                        real_data[REALTIME_BID_SELL_LIST[2 * i]][j]) * common.get_float_value(
                        real_data[REALTIME_BID_SELL_LIST[2 * i + 1]][j])
                    if amount * 100 >= MONITOR_THRESHOLD_AMOUNT:
                        real_pressure_data = real_data[j:j + 1]
                        save_pressure_data(connection, real_pressure_data)
                        print 'sell pressure deal: ', stock_code[j]
                        break
        except Exception as e:
            print(e)
            continue
        except:
            print("Error: ", stock_code)
            continue


def save_pressure_data(connection, real_pressure_data):
    raw_data = real_pressure_data[RECORD_FORMAT].values
    date_time = common.get_format_datetime(raw_data[0][-2], raw_data[0][-1])
    data_list = list(raw_data[0][:-2])
    data_list.append(date_time)
    data_tuple = tuple(data_list)
    db.add_pressure_monitor_data(connection, data_tuple)
