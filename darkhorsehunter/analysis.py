# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 16:11:15 2016

@author: claude
"""

import pandas as pd
import util.common as common
import util.dbtools as db


def check_pressure_deal(pressure_detail_list):
    detail_code = pressure_detail_list.ix[0]['code']
    detail_name = pressure_detail_list.ix[0]['name']
    detail_datetime = pressure_detail_list.ix[0]['datetime']

    tmp_pressure_times = 0
    tmp_pressure_amount = 0
    pressure_price = 0

    for i in pressure_detail_list.index:
        detail = get_pressure_value(pressure_detail_list.ix[i])

        if pressure_price != common.get_float_value(detail['pressure_price'].values[0]):
            tmp_pressure_times += 1

            if tmp_pressure_amount < common.get_float_value(detail['total_amounts'].values[0]):
                tmp_pressure_amount = common.get_float_value(detail['total_amounts'].values[0])
                pressure_price = common.get_float_value(detail['pressure_price'].values[0])

    return pd.DataFrame({"code": [detail_code], "name": [detail_name], "times": [tmp_pressure_times],
                         "datetime": [detail_datetime], "amount": tmp_pressure_amount / 100})


def get_pressure_value(pressure_detail):
    pressure_amount = common.get_float_value(pressure_detail['sell_amount1'])
    pressure_price = common.get_float_value(pressure_detail['sell_price1'])

    if (pressure_amount * pressure_price < common.get_float_value(
            pressure_detail['sell_amount2']) * common.get_float_value(
            pressure_detail['sell_price2'])):
        pressure_amount = pressure_detail['sell_amount2']
        pressure_price = pressure_detail['sell_price2']

    elif (pressure_amount * pressure_price < common.get_float_value(
            pressure_detail['sell_amount3']) * common.get_float_value(
            pressure_detail['sell_price3'])):
        pressure_amount = pressure_detail['sell_amount3']
        pressure_price = pressure_detail['sell_price3']

    elif (pressure_amount * pressure_price < common.get_float_value(
            pressure_detail['sell_amount4']) * common.get_float_value(
            pressure_detail['sell_price4'])):
        pressure_amount = pressure_detail['sell_amount4']
        pressure_price = pressure_detail['sell_price4']

    elif (pressure_amount * pressure_price < common.get_float_value(
            pressure_detail['sell_amount5']) * common.get_float_value(
            pressure_detail['sell_price5'])):
        pressure_amount = pressure_detail['sell_amount5']
        pressure_price = pressure_detail['sell_price5']

    return pd.DataFrame({"code": [pressure_detail['code']], "name": [pressure_detail['name']],
                         "pressure_amount": [pressure_amount], "pressure_price": [pressure_price],
                         "total_amounts": [
                             common.get_float_value(pressure_amount) * common.get_float_value(pressure_price)]})


def analysis(conn, engine):
    stock_code_list = db.get_pressure_stock_list(conn)

    for code in stock_code_list:
        pressure_detail_list = db.get_analysis_pressure(conn, code)
        df = check_pressure_deal(pressure_detail_list)
        df.to_sql('analysis_results', engine, index=False, if_exists='append')
        print df
