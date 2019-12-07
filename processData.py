# Need to take the transpose of the getStocks data and return a CSV with the values.
# Need to also consider cases when there is missing stock data if any (median filling or whatever).

import glob, os
import re
import pandas as pd
import zipfile
from datetime import datetime
import numpy as np


def extractData():
    for file in glob.glob("stockData/*.zip"):
        print("processData is extracting " + file)
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall("./stockData")
        print("processData is deleting " + file)
        os.remove(file)

def unifyCSV(columns_to_extract):
    stockDF = pd.DataFrame(columns = columns_to_extract)
    for file in glob.glob("stockData/*.csv"):
        tmp = pd.read_csv(file)
        print("processData is unifying: " + file)
        stockDF = stockDF.append(tmp[columns_to_extract])
        print("processData is deleting: " + file)
        os.remove(file)
    return stockDF

def getQuoteTable(symbols, stockDF, params=[]):
    if symbols == "ALL":
        symbols = list(set(stockDF['SYMBOL'].tolist()))
    table_columns = ['DATE']
    for i in symbols:
        table_columns = table_columns + [str(i)]
    quoteTable = pd.DataFrame(columns=table_columns)
    stockAgg = []
    for x in list(map(lambda y: y.strftime('%d-%b-%Y').upper(), sorted(list(map(lambda x: datetime.strptime(x, '%d-%b-%Y'), list(set(stockDF['TIMESTAMP']))))))):
        row = []
        row.append(x)
        for j in [y for y in quoteTable.columns if y != 'DATE']:
            residue = stockDF[(stockDF['SYMBOL'] == j) & (stockDF['TIMESTAMP'] == x)]['CLOSE'].tolist()
            if len(residue) == 0:
                residue = np.NaN
            else:
                residue = residue[0]
            row.append(residue)
        stockAgg.append(row)
    quoteTable = pd.DataFrame(stockAgg, columns = table_columns)
    return quoteTable





