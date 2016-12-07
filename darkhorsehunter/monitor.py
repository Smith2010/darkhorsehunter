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
PRICE_LIST = ['open', 'pre_close', 'price', 'high', 'low']
RECORD_FORMAT = ['code', 'name'] + PRICE_LIST + REALTIME_BID_SELL_LIST + REALTIME_BID_BUY_LIST + ['date', 'time']

MONITOR_THRESHOLD_AMOUNT = 5000000
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
                price = common.get_decimal_value(real_data['price'][j])
                pre_close = common.get_decimal_value(real_data['pre_close'][j])
                change_rate = ((price / pre_close) - 1) * 100

                if change_rate > 9.5 or change_rate < -9.5:
                    continue

                for i in range(0, 5):  # sell
                    sell_price = common.get_decimal_value(real_data[REALTIME_BID_SELL_LIST[2 * i]][j])
                    sell_volume = common.get_decimal_value(real_data[REALTIME_BID_SELL_LIST[2 * i + 1]][j])
                    sell_amount = sell_price * sell_volume * 100

                    if sell_amount >= MONITOR_THRESHOLD_AMOUNT:
                        save_pressure_data(connection, real_data[j:j + 1])
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

    data_list = list(raw_data[0])
    for idx in range(len(data_list)):
        if data_list[idx] == '':
            data_list[idx] = 0

    data_list[-2] = common.get_format_date(data_list[-2])
    db.add_pressure_monitor_data(connection, data_list)
