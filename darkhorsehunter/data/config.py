# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 17:21:14 2016

@author: claude
"""

import os

MAX_MONITOR_STOCK_NUM = 1000
THRESHOLD_OUTSTANDING = 5000
REALTIME_BASIC_LIST = ['code', 'name', 'price', 'bid', 'ask', 'volume', 'amount', 'time']
REALTIME_BID_BUY_LIST = ['b1_p', 'b1_v', 'b2_p', 'b2_v', 'b3_p', 'b3_v', 'b4_p', 'b4_v', 'b5_p', 'b5_v']
REALTIME_BID_SELL_LIST = ['a1_p', 'a1_v', 'a2_p', 'a2_v', 'a3_p', 'a3_v', 'a4_p', 'a4_v', 'a5_p', 'a5_v']
RECORD_FORMAT = ['code', 'name'] + REALTIME_BID_SELL_LIST + REALTIME_BID_BUY_LIST + ['date', 'time']
MONITOR_THRESHOLD_AMOUNT = 10000000

host = os.getenv('DARKHORSE_HOST')
user = os.getenv('DARKHORSE_USER')
passwd = os.getenv('DARKHORSE_PASSWD')
db = os.getenv('DARKHORSE_DB')
