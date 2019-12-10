# We will use CoinCap API V2.0 to get the 10 minute interval data across different exchanges.

import time
import requests
import ast
from datetime import datetime


def mtime2dt(mtime):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))

def dt2mtime(tstamp):
    # tstamp = (day, month, year, hours, minutes, seconds)
    year = tstamp[2]; month = tstamp[1]; day = tstamp[0]
    hours = tstamp[3]; minutes = tstamp[4]; seconds = tstamp[5]
    tstring = str(year)+"-"+str(month)+"-"+str(day)+" "+str(hours)+":"+str(minutes)+":"+str(seconds)
    dtobject = datetime.strptime(tstring, "%Y-%m-%d %H:%M:%S")
    return int(dtobject.timestamp()*1000)

def getData(exchange, frequency, baseAsset, quoteAsset, startTime, endTime):
    # We need start-time and end-time to be in the six-tuple format of (day, mon, year, hr, min, sec). 
    url = "https://api.coincap.io/v2/candles?exchange="+str(exchange)+"&interval="+str(frequency)+"&baseId="+str(baseAsset)+"&quoteId="+str(quoteAsset)+"&start="+str(dt2mtime(startTime))+"&end="+str(dt2mtime(endTime))
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    payload = {}
    response = requests.request("GET", url, headers=headers, data = payload)
    print("getData is processing request " + str(url))
    return ast.literal_eval(response.text)


def unifyQuoteDict(quoteDict):



