# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 16:11:15 2016

@author: claude
"""

import pandas as pd
import util.common as common
import util.dbtools as db

RECORD_FORMAT = ['id', 'code', 'name', 'change_rate', 'price', 'amount', 'outstandMarketValue', 'today_times', 'days',
                 'datetime']


def check_pressure_deal(pressure_detail_list, outstanding_market_value, pressure_days):
    detail_code = pressure_detail_list.ix[0]['code']
    detail_name = pressure_detail_list.ix[0]['name']
    detail_pre_close = pressure_detail_list.ix[0]['pre_close']

    date = pressure_detail_list.ix[0]['datetime'][0:8]
    result_id = common.get_int_value(date + detail_code)

    today_times = 0
    pressure_amount = 0
    pressure_price = 0
    pressure_datetime = ''

    for i in pressure_detail_list.index:
        detail = get_pressure_value(pressure_detail_list.ix[i])

        if pressure_price != detail['pressure_price'].values[0]:
            today_times += 1

            if pressure_amount < detail['total_amounts'].values[0]:
                pressure_amount = detail['total_amounts'].values[0]
                pressure_price = detail['pressure_price'].values[0]
                pressure_datetime = detail['datetime'].values[0]

    pressure_change_rate = (pressure_price / detail_pre_close - 1) * 100

    return pd.DataFrame({"id": [result_id], "code": [detail_code], "name": [detail_name],
                         "change_rate": [round(pressure_change_rate, 2)], "price": [pressure_price],
                         "amount": [round(pressure_amount / 100, 0)], "outstandMarketValue": [outstanding_market_value],
                         "today_times": [today_times], "days": [pressure_days], "datetime": [pressure_datetime]})


def get_pressure_value(pressure_detail):
    pressure_datetime = pressure_detail['datetime']
    pressure_amount = pressure_detail['sell_amount1']
    pressure_price = pressure_detail['sell_price1']

    if pressure_amount * pressure_price < pressure_detail['sell_amount2'] * pressure_detail['sell_price2']:
        pressure_amount = pressure_detail['sell_amount2']
        pressure_price = pressure_detail['sell_price2']

    elif pressure_amount * pressure_price < pressure_detail['sell_amount3'] * pressure_detail['sell_price3']:
        pressure_amount = pressure_detail['sell_amount3']
        pressure_price = pressure_detail['sell_price3']

    elif pressure_amount * pressure_price < pressure_detail['sell_amount4'] * pressure_detail['sell_price4']:
        pressure_amount = pressure_detail['sell_amount4']
        pressure_price = pressure_detail['sell_price4']

    elif pressure_amount * pressure_price < pressure_detail['sell_amount5'] * pressure_detail['sell_price5']:
        pressure_amount = pressure_detail['sell_amount5']
        pressure_price = pressure_detail['sell_price5']

    return pd.DataFrame({"pressure_amount": [pressure_amount], "pressure_price": [pressure_price],
                         "total_amounts": [pressure_amount * pressure_price], "datetime": [pressure_datetime]})


def analysis(conn):
    stock_code_list = db.get_today_pressure_stocks(conn)

    for stock_code in stock_code_list:
        try:
            out_market_value = db.get_stock_outstanding_market_value(conn, stock_code)
            days = 0
            pressure_detail_list = db.get_today_pressure_data(conn, stock_code)
            analysis_results = check_pressure_deal(pressure_detail_list, out_market_value, days)

            raw_data = analysis_results[RECORD_FORMAT].values
            db.add_analysis_results_data(conn, list(raw_data[0]))
            print analysis_results
        except Exception as e:
            print(e)
            continue
        except:
            print("Error: ", stock_code)
            continue
