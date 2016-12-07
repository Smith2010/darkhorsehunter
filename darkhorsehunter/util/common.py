# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 14:19:27 2016

@author: claude
"""

import datetime as dt


def get_int_value(number):
    """
    string to int
    """
    return int(number) if is_int(number) else 0


def get_float_value(number):
    """
    string to float
    """
    return float(number) if is_float(number) else 0


def is_int(number):
    try:
        int(number)
        return True
    except ValueError:
        return False


def is_float(number):
    try:
        float(number)
        return True
    except ValueError:
        return False


def get_format_current_time():
    return dt.datetime.now().strftime("%Y%m%d%H%M%S")


def get_format_datetime(date_value, time_value):
    return date_value[0:4] + date_value[5:7] + date_value[8:10] + time_value[0:2] + time_value[3:5] + time_value[6:8]

