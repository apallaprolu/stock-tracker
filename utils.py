#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 18:49:49 2019

@author: apallaprolu
"""

#Utilities for getCrypto


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



def to_xy(df, y, filterNAN=False, scale=1):
    # Filter NANs and list data in increasing order of time growth.
    # Scale is default in milliseconds => harder to predict.
    x = list(map(lambda t: datetime.strptime(t, "%Y-%m-%d %H:%M:%S"), list(df.index)))
    xDiff = []
    for i in range(1, len(x)):
        try:
            xDiff.append(((x[i] - x[0]).total_seconds())/(scale))
        except:
            continue
    y_axis = df[y].values.tolist()
    nanTimeStamps = []
    del y_axis[0]
    
    if filterNAN:
        nanIndices = []
        for i in range(len(y_axis)):
            if str(y_axis[i]) == "nan":
                nanIndices.append(i)
                
        xFinal, yFinal = [], []
            
        for i in range(len(y_axis)):
            if i not in nanIndices:
                xFinal.append(xDiff[i])
                yFinal.append(y_axis[i])
            else:
                nanTimeStamps.append(xDiff)
        return xFinal, yFinal, nanTimeStamps
    else:
        return xDiff, y_axis, nanTimeStamps



def mtime2dt(mtime):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))

def dt2mtime(tstamp):
    # tstamp = (day, month, year, hours, minutes, seconds)
    year = tstamp[2]; month = tstamp[1]; day = tstamp[0]
    hours = tstamp[3]; minutes = tstamp[4]; seconds = tstamp[5]
    tstring = str(year)+"-"+str(month)+"-"+str(day)+" "+str(hours)+":"+str(minutes)+":"+str(seconds)
    dtobject = datetime.strptime(tstring, "%Y-%m-%d %H:%M:%S")
    return int(dtobject.timestamp()*1000)

def getTimeMatch(seek, searchList):
    for i in searchList:
        if i[0] == seek:
            return i[1]
    return np.NaN

def sortTimestampStr(listOfTimestampStr):
    globalTimeLine_dtMap = list(map(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"), listOfTimestampStr))
    globalTimeLine_dtMap.sort()
    globalTimeLine = list(map(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"), globalTimeLine_dtMap))
    return globalTimeLine