# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 16:11:15 2016

@author: claude
"""

import MySQLdb

from main.data.config import *
from main.util.dbtools import *
from sqlalchemy import create_engine


def check_pressure_deal(pressure_detail_list):
    detail_code = pressure_detail_list.ix[0]['code']
    detail_name = pressure_detail_list.ix[0]['name']
    detail_datetime = pressure_detail_list.ix[0]['datetime']

    tmp_pressure_times = 0
    tmp_pressure_amount = 0
    pressure_price = 0

    for i in pressure_detail_list.index:
        detail = get_pressure_value(pressure_detail_list.ix[i])

        if (pressure_price != float(detail['pressure_price'].values[0])):
            tmp_pressure_times = tmp_pressure_times + 1

            if (tmp_pressure_amount < float(detail['total_amounts'].values[0])):
                tmp_pressure_amount = float(detail['total_amounts'].values[0])
                pressure_price = float(detail['pressure_price'].values[0])

    return pd.DataFrame({"code": [detail_code], "name": [detail_name], "times": [tmp_pressure_times],
                         "datetime": [detail_datetime], "amount": tmp_pressure_amount})


def get_pressure_value(pressure_detail):
    pressure_amount = float(pressure_detail['sell_amount1'])
    pressure_price = float(pressure_detail['sell_price1'])

    if (pressure_amount * pressure_price < float(pressure_detail['sell_amount2']) * float(
            pressure_detail['sell_price2'])):
        pressure_amount = pressure_detail['sell_amount2']
        pressure_price = pressure_detail['sell_price2']

    elif (pressure_amount * pressure_price < float(pressure_detail['sell_amount3']) * float(
            pressure_detail['sell_price3'])):
        pressure_amount = pressure_detail['sell_amount3']
        pressure_price = pressure_detail['sell_price3']

    elif (pressure_amount * pressure_price < float(pressure_detail['sell_amount4']) * float(
            pressure_detail['sell_price4'])):
        pressure_amount = pressure_detail['sell_amount4']
        pressure_price = pressure_detail['sell_price4']

    elif (pressure_amount * pressure_price < float(pressure_detail['sell_amount5']) * float(
            pressure_detail['sell_price5'])):
        pressure_amount = pressure_detail['sell_amount5']
        pressure_price = pressure_detail['sell_price5']

    return pd.DataFrame({"code": [pressure_detail['code']], "name": [pressure_detail['name']],
                         "pressure_amount": [pressure_amount], "pressure_price": [pressure_price],
                         "total_amounts": [float(pressure_amount) * float(pressure_price)]})


conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset="utf8")
engine = create_engine('mysql://' + user + ':' + passwd + '@' + host + '/' + db + '?charset=utf8')

stockCodeList = get_pressure_stock_list(conn)


for code in stockCodeList:
    pressureDetailList = get_analysis_pressure(conn, code)
    df = check_pressure_deal(pressureDetailList)
    df.to_sql('analysis_results', engine, index=False, if_exists='append')
    print df

conn.close()
engine.connect().close()



