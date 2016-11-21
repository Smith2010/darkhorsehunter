# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 12:23:26 2016

@author: oncast
Filter the
"""
from main.utiliy.dbUtil import *
from main.utiliy.NormalUtil import *

def JudgePressure(moniStockDetail):
    tmp_pressure_times = 0
    tmp_pressure_amout = 0
    cloumns=['code','name','pressure_amout','pressure_times']
    codes=[]
    names=[]
    pressure_amouts=[]
    pressure_times=[]


while(i< code_list.size):
        moniStockDetail = GetAnyaysisPressure(con,'20161119',code_list.values[i][0])
        print moniStockDetail
        i =i +1
#        pressures = GedAnyaysisPressure(con,code)