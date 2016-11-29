# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 12:23:26 2016

@author: oncast
"""

import pandas as pd
import tushare as ts
import datetime as dt
import sqlalchemy
import util.env as env

TOTAL_ASSERT_LIMIT = 500000
X_DAYS_AGO = 30

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

AgostrDate = (dt.datetime.now() - dt.timedelta(days=X_DAYS_AGO)).strftime("%Y%m%d")
infoList = ts.get_stock_basics()


def get_available_stock():
    try:
        for stockCode in infoList.index:
            stock = infoList.ix[stockCode]

            if (stock['outstanding'] == 0):
                continue

            if (int(stock['timeToMarket']) > int(AgostrDate)):
                continue

            try:
                real_data = ts.get_realtime_quotes(stockCode)
            except:
                print("Error: ", stockCode)
                continue

            if (real_data is None):
                continue

            outstand_market_value = stock['outstanding'] * float(real_data['price'].values[0]) * 10000
            total_market_value = stock['totals'] * float(real_data['price'].values[0]) * 10000
            real_market_value = outstand_market_value
            if (real_market_value > 0 and real_market_value < TOTAL_ASSERT_LIMIT):
                print stockCode
                code.append(stockCode)
                name.append(stock['name'])
                industry.append(stock['industry'])
                outstanding.append(stock['outstanding'])
                totalAssets.append(stock['totalAssets'])
                fixedAssets.append(stock['fixedAssets'])
                liquidAssets.append(stock['liquidAssets'])
                totalMarketValue.append(total_market_value)
                outstandMarketValue.append(outstand_market_value)
                realMarketValue.append(real_market_value)

        print code

        df2 = pd.DataFrame({"code": pd.Series(code), "name": pd.Series(name), "industry": pd.Series(industry),
                            "outstanding": pd.Series(outstanding), "totalAssets": pd.Series(totalAssets),
                            "fixedAssets": pd.Series(fixedAssets), "liquidAssets": pd.Series(liquidAssets),
                            "totalMarketValue": pd.Series(totalMarketValue),
                            "outstandMarketValue": pd.Series(outstandMarketValue),
                            "realMarketValue": pd.Series(realMarketValue)})

        print df2
        return df2

    except TypeError as e:
        print 'here is end ', e


print 'Init stock pool start: ', dt.datetime.now()

df = get_available_stock()

engine = sqlalchemy.create_engine('mysql://' + env.user + ':' + env.passwd + '@' + env.host + '/' + env.db + '?charset=utf8')
df.to_sql('stock_pool', engine, index=False, if_exists='append')
engine.connect().close()

print 'Init stock pool end: ', dt.datetime.now()
