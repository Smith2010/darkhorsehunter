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
        insert_sql = "insert into pressure_monitor (code, name, sell_price1, sell_amount1, sell_price2, sell_amount2," \
                     " sell_price3, sell_amount3, sell_price4, sell_amount4, sell_price5, sell_amount5," \
                     " buy_price1, buy_amount1, buy_price2, buy_amount2, buy_price3, buy_amount3," \
                     " buy_price4, buy_amount4, buy_price5, buy_amount5, datetime) " \
                     " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(insert_sql, values)
        cur.close()
        connection.commit()
        return 0
    except IOError as e:
        print (e)
        return None


def get_pressure_stock_list(conn):
    try:
        codes = []
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


def get_analysis_pressure(conn, code):
    try:
        query_sql = "select * from pressure_monitor " \
                    "where code='" + code + "' and create_datetime>=date(now()) " \
                    "and create_datetime<DATE_ADD(date(now()),INTERVAL 1 DAY) order by create_datetime"
        return pd.read_sql(query_sql, conn)
    except IOError as e:
        print (e)
        return None
