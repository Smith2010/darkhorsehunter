# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 12:23:26 2016

@author: oncast
"""
import tushare as ts
import pandas as pd
import datetime

from sqlalchemy import create_engine

TOTAL_ASSERT_LIMIT = 500000
X_DAYS_AGO = 30

info = ts.get_stock_basics()
AgostrDate = (datetime.datetime.now() - datetime.timedelta(days=X_DAYS_AGO)).strftime("%Y%m%d")

indexs = []

cloumns = ['code', 'name', 'industry', 'outstanding', 'totalAssets', 'fixedAssets', 'liquidAssets', 'totalMarketValue',
           'outstandMarketValue', 'realMarketValue']
code = []
name = []
industry = []
outstanding = []
totalAssets = []
fixedAssets = []
liquidAssets = []
totalMarketValue = []
outstandMarketValue = []
realMarketValue = []


def loop_all_stocks():
    i = 0
    try:
        for EachStockID in info.index:
            if (info.ix[EachStockID]['outstanding'] == 0):
                continue
            if (int(info.ix[EachStockID]['timeToMarket']) > int(AgostrDate)):
                continue
            if (ts.get_realtime_quotes(EachStockID) is None):
                continue
            outstand_market_value = info.ix[EachStockID]['outstanding'] * float(
                ts.get_realtime_quotes(EachStockID)['price'].values[0])
            total_market_value = info.ix[EachStockID]['totals'] * float(
                ts.get_realtime_quotes(EachStockID)['price'].values[0])
            real_market_value = outstand_market_value
            if (real_market_value < TOTAL_ASSERT_LIMIT and real_market_value > 0):
                indexs.append(i)
                code.append(EachStockID)
                name.append(info.ix[EachStockID]['name'])
                industry.append(info.ix[EachStockID]['industry'])
                outstanding.append(info.ix[EachStockID]['outstanding'])
                totalAssets.append(info.ix[EachStockID]['totalAssets'])
                fixedAssets.append(info.ix[EachStockID]['fixedAssets'])
                liquidAssets.append(info.ix[EachStockID]['liquidAssets'])
                totalMarketValue.append(total_market_value)
                outstandMarketValue.append(outstand_market_value)
                realMarketValue.append(real_market_value)
                i += 1

        print code
        df = pd.DataFrame({"code": pd.Series(code), "name": pd.Series(name), "industry": pd.Series(industry),
                           "outstanding": pd.Series(outstanding),
                           "totalAssets": pd.Series(totalAssets), "fixedAssets": pd.Series(fixedAssets),
                           "liquidAssets": pd.Series(liquidAssets),
                           "totalMarketValue": pd.Series(totalMarketValue),
                           "outstandMarketValue": pd.Series(outstandMarketValue),
                           "realMarketValue": pd.Series(realMarketValue)})
        print df
        return df
    except TypeError:
        print 'here is end ', EachStockID
        return df


print datetime.datetime.now()
df = loop_all_stocks()
print datetime.datetime.now()
engine = create_engine('mysql://root:@127.0.0.1/darkhorsedb?charset=utf8')
df.to_sql('stock_pool', engine)




