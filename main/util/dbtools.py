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
    except IOError:
        return None


def add_pressure_monitor_data(connection, values):
    try:
        cur = connection.cursor()
        insert_sql = "insert into pressure_monitor values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(insert_sql, values)
        cur.close()
        connection.commit()
        return 0
    except IOError:
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
    except IOError:
        return None


def get_analysis_pressure(conn, code):
    try:
        query_sql = "select * from pressure_monitor " \
                    "where code='" + code + "' " \
                    "and create_datetime>=date(now()) " \
                    "and create_datetime<DATE_ADD(date(now()),INTERVAL 1 DAY) " \
                    "order by create_datetime"
        return pd.read_sql(query_sql, conn)
    except IOError:
        return None
