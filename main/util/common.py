# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 14:19:27 2016

@author: claude
"""

import datetime as dt
import time


def get_value(number):
    """
    string to float
    """
    try:
        return float(number)
    except ValueError:
        return 0


def get_format_current_time():
    return dt.datetime.now().strftime("%Y%m%d%H%M%S")


def get_format_datetime(date_value, time_value):
    return date_value[0:4] + date_value[5:7] + date_value[8:10] + time_value[0:2] + time_value[3:5] + time_value[6:8]


def deco(func):
    def _deco(*args, **kwargs):

        print "Begin ", dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        res = func(*args, **kwargs)
        time.sleep(5)

        return res

    return _deco
