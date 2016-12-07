# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 16:11:15 2016

@author: claude
"""

import pandas as pd


def get_db_value(conn, sql):
    """
    SQL to dataframe
    """
    try:
        return pd.read_sql(sql, conn)
    except IOError as e:
        print (e)
        return None


def add_pressure_monitor_data(connection, values):
    try:
        cur = connection.cursor()
        insert_sql = "insert into pressure_monitor (code, name, open, pre_close, price, high, low, " \
                     " sell_price1, sell_volume1, sell_price2, sell_volume2, sell_price3, sell_volume3, " \
                     " sell_price4, sell_volume4, sell_price5, sell_volume5," \
                     " buy_price1, buy_volume1, buy_price2, buy_volume2, buy_price3, buy_volume3," \
                     " buy_price4, buy_volume4, buy_price5, buy_volume5, pressure_date, pressure_time) " \
                     " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(insert_sql, values)
        cur.close()
        connection.commit()
        return 0
    except IOError as e:
        print (e)
        return None


def get_today_pressure_stocks(conn):
    codes = []
    try:
        cur = conn.cursor()
        query_sql = "select distinct(code) from pressure_monitor " \
                    "where create_datetime>=date(now()) " \
                    "and create_datetime<DATE_ADD(date(now()),INTERVAL 1 DAY)"
        dfs = cur.execute(query_sql)
        results = cur.fetchmany(dfs)
        for item in results:
            codes.append(item[0])
        cur.close()
        return codes
    except IOError as e:
        print (e)
        return None


def get_stock_outstanding_market_value(conn, code):
    value = 0
    try:
        cur = conn.cursor()
        query_sql = "select outstandMarketValue from stock_pool where code=%s" % code
        dfs = cur.execute(query_sql)
        results = cur.fetchmany(dfs)
        for item in results:
            value = item[0]
        cur.close()
        return value
    except IOError as e:
        print (e)
        return None


def get_today_pressure_data(conn, code):
    query_sql = "select * from pressure_monitor where code=%s and create_datetime>=date(now()) " \
                "and create_datetime<DATE_ADD(date(now()),INTERVAL 1 DAY) order by create_datetime desc" % code
    return get_db_value(conn, query_sql)


def add_analysis_results_data(connection, values):
    try:
        cur = connection.cursor()
        insert_sql = "insert into analysis_results (id, code, name, change_rate, price, amount, outstandMarketValue, " \
                     " today_times, days, pressure_date, pressure_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) " \
                     " on duplicate key update " \
                     " change_rate=VALUES(change_rate), " \
                     " price=VALUES(price), " \
                     " amount=VALUES(amount), " \
                     " today_times=VALUES(today_times), " \
                     " pressure_time=VALUES(pressure_time)"
        cur.execute(insert_sql, values)
        cur.close()
        connection.commit()
        return 0
    except IOError as e:
        print (e)
        return None
