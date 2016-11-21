# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 15:27:52 2016

@author: claude
"""

from monitor import *

if __name__ == "__main__":
    df = GetDbValue(conn, sql_stock_pool)
    Monitor(conn, df, MAX_MONITOR_STOCK_NUM)
    conn.close();
