# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 16:11:15 2016

@author: oncast
"""

import tushare as ts
import datetime
import MySQLdb
import pandas as pd
import time


def GetFormatNowTime():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def GetFormatdatetime(date, time):
    return date[0:4] + date[5:7] + date[8:10] + time[0:2] + time[3:5] + time[6:8]

def GetValue(number):
    """
    string to float
    """
    try:
        return float(number)
    except ValueError:
        return 0

def deco(func):
    def _deco(*args, **kwargs):
        print "Begin",
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
        print otherStyleTime
        res = func(*args, **kwargs)
        time.sleep(5)
        return  res
    return _deco