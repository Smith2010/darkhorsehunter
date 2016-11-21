# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 17:21:14 2016

@author: claude
"""

from MySQLdb import connect

MAX_MONITOR_STOCK_NUM = 100
THRESH_HOLD_OUTSTANDING = 5000
REALTIME_BASIC_LIST = ['code','name','price','bid','ask','volume','amount','time']
REALTIME_BID_BUY_LIST = ['b1_v', 'b1_p', 'b2_v', 'b2_p', 'b3_v', 'b3_p', 'b4_v', 'b4_p', 'b5_v', 'b5_p']
REALTIME_BID_SELL_LIST = ['a1_v', 'a1_p', 'a2_v', 'a2_p', 'a3_v', 'a3_p', 'a4_v', 'a4_p', 'a5_v', 'a5_p']
RECORD_FORMAT=['code','name'] + REALTIME_BID_BUY_LIST + REALTIME_BID_SELL_LIST + ['date', 'time']
THRESH_AMOUNT = 5000000
conn = connect(host="106.14.42.175",user="duser",passwd="1qaz@WSX",db="darkhorse",charset="utf8")
sql_stock_pool = "select * from stock_pool"