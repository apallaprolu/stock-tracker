#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 11:58:31 2019

@author: apallaprolu
"""

# Powered by CoinGecko API
# Most transaction details are in GMT time standard. We need to watch out about this.


from pycoingecko import CoinGeckoAPI
from itertools import chain
from datetime import datetime
import time

import pandas as pd
import numpy as np
import random
import json
import copy

import scipy.io
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, ExtraTreesRegressor
from sklearn.linear_model import SGDRegressor
from scipy import interpolate
    
from sklearn.model_selection import train_test_split
import sklearn.metrics as met
import matplotlib.pyplot as plt

from utils import *

    
# We need to pick the following for analysis:
# 1. Coins to trade: Bitcoin, Ethereum, Litecoin, Ripple, Stellar
# 2. Stablecoins to base these purchases on. 
# 3. Markets where these coins are being traded/exchanged and their historical data. 

# Some interesting API calls:

# get_coin_market_chart_by_id => arguments: quoteAsset, baseAsset, days_in_the_past
# If days < 1, you get per minute granular data.
# If days < 90, you get per hour granular data.
# If days > 90, you get daily granular data.
    
# get_coin_history_by_id => arguments: quoteAsset, dd-mm-yyyy
# Gives valuation across a whole range of international currencies.
# Gives market_cap, volume_data as well across the same currencies. 
# Additionally gives information about Twitter followers, et cetera for sentiment analysis maybe. 

def getCryptoVsUSD(coins, days):
    resDict = {}
    cg = CoinGeckoAPI()
    print("getCryptoVsUSD is pinging CoinGeckoAPI")
    try:
        cg.ping()
    except:
        print("getCryptoVsUSD has died due to lack of connection")
        return -1
    print("getCryptoVsUSD succesfully reached CoinGeckoAPI.")
    for coin in coins:
        tmpDict = cg.get_coin_market_chart_by_id(coin, "usd", days)
        tmpDict["prices."+str(coin)] = list(map(lambda x: [mtime2dt(x[0]/1000), x[1]], tmpDict["prices"]))
        tmpDict["market_caps."+str(coin)] = list(map(lambda x: [mtime2dt(x[0]/1000), x[1]], tmpDict["market_caps"]))
        tmpDict["total_volumes."+str(coin)] = list(map(lambda x: [mtime2dt(x[0]/1000), x[1]], tmpDict["total_volumes"]))
        del tmpDict["prices"]; del tmpDict["market_caps"]; del tmpDict["total_volumes"]
        resDict = {**resDict, **tmpDict}
    
    # We need to use the data in resDict to construct the time ordered table for the coins
    # Hpwever, it is very likely that there won't be any concurrency
    
    globalTimeLine = []
    
    for key in resDict.keys():
        globalTimeLine.append(list(map(lambda x: x[0], resDict[key])))
    
    globalTimeLineForDebug = copy.deepcopy(globalTimeLine)
    
    globalTimeLine = sortTimestampStr(list(set(chain.from_iterable(globalTimeLine))))
    
    # If there is a datapoint in any of the dictionary values, insert it in the corresponding row.
    # The rows will be coming from a list-of-lists and the columns will be the keys of the dictionary.
    # Missing data will be np.NaN, which we will then interpolate using different strategies.
    
    tableRows = []
    for i in globalTimeLine:
        tmpRow = [i]
        for key in resDict.keys():
            tmpRow.append(getTimeMatch(i, resDict[key]))
        tableRows.append(tmpRow)
    
    colsDF = ['timestamp'] + list(resDict.keys())
    retDF = pd.DataFrame(tableRows, columns=colsDF)
    retDF.index = retDF['timestamp']
    retDF.drop('timestamp', axis=1)
    
    # We need to use the univariate splines to fill in intermittent data. 
    # This is the only way out and we assume that the market volatility is stable for ~ 20seconds.
    
    # We need to check other methods of interpolation (ref: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.interpolate.html)
    
    return retDF.interpolate(method="linear"), globalTimeLineForDebug
    
        
def trainStrategy(pcv_DF, column, nDays, strategy="SGD"):
 
    # We need to use RandomForest on imbalanced dataset to predict accurate values.
    # Since the timeline is consistent across valid datapoints, we can use a single strategy.
    
    # Time to shine, black swans.
   
    tmpx, tmpy, nanTS = to_xy(pcv_DF, column, filterNAN=True, scale=nDays*24*3600) #normalize it to number of days
    # tmpx will be a number between 0 to 1, and gets closer to the terminal date 
    
    if strategy == "SGD":
        x_train, x_test, y_train, y_test = train_test_split(tmpx, tmpy, test_size=0.4, shuffle=False)
        print(x_train[0], x_train[-1])
        print(x_test[0], x_test[-1])
        x_train, y_train = np.asarray(x_train), np.asarray(y_train)
        mdl = SGDRegressor(shuffle=True, max_iter=100000, learning_rate='optimal', random_state=random.randint(1, 100), n_iter_no_change=30)
        mdl.fit(x_train.reshape(-1, 1), y_train.reshape(-1, 1))
        y_pred = mdl.predict(np.asarray(x_test).reshape(-1, 1))
#        for i in range(len(y_pred)):
#            print(y_pred[i], y_test[i], x_test[i])
        print("RMSE: " + str(np.sqrt(met.mean_squared_error(y_pred, y_test))))
        print("RMSE/MEAN: " + str(np.sqrt(met.mean_squared_error(y_pred, y_test))/np.mean(y_test)))
    elif strategy == "INP":
        # Cubic spline interpolation. 
        # This obviously cannot predict into the future but does a fab job filling up the missing details.
        # We can use this for minutely interval prediction from half hour windows.
        
        coordinates = list(zip(tmpx, tmpy))
        print(coordinates)
        return 0
        
        cs = interpolate.CubicSpline(np.asarray(tmpx[0:int(0.9999*len(tmpx))]), np.asarray(tmpy[0:int(0.9999*len(tmpy))]))
        y_pred = np.asarray(list(map(lambda x: cs(x), tmpx[int(0.4*len(tmpx)):])))
        for i in range(len(tmpx[int(0.4*len(tmpx)):])):
            print(y_pred[i], tmpy[int(0.4*len(tmpy)):][i], tmpx[int(0.4*len(tmpx)):][i])
        print("RMSE: " + str(np.sqrt(met.mean_squared_error(y_pred, tmpy[int(0.4*len(tmpy)):]))))
        print("RMSE/MEAN: " + str(np.sqrt(met.mean_squared_error(y_pred, tmpy[int(0.4*len(tmpy)):]))/np.mean(tmpy[int(0.4*len(tmpy)):])))
    elif strategy == "RFR":
        pass
    elif strategy == "XGB":
        pass
    
        
#    filteredSets = []
#    
#    for col in list(pcv_DF.columns):
#        
#        filteredSets.append((col, tmpx, tmpy, nanTS))
#           
#    # filteredSets consists of tuples that will be trained.
#    
#    x_train, x_test, y_train, y_test = train_test_split(filteredSets[0][1], filteredSets[0][2], test_size=0.15, shuffle=False)
#    
#    # Univariate spline => straight line interpolation. Not good for datasets with high variance.
#    pred_model = interpolate.UnivariateSpline(x_train, y_train, s=2)
#    RMSE = []
#
#    for i in range(len(x_test)):
#        RMSE.append((y_test[i] - pred_model(x_test[i]))**2)
#        print(x_test[i], y_test[i], pred_model(x_test[i]))
#    RMSE = np.sqrt(sum(RMSE)/len(RMSE))
#    print("Error reported: " + str(RMSE))

        
            
        
        
        
    
      
        
        
    
    
    



