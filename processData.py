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
    os.rmdir("stockData")
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
        print("getQuoteTable is processing timestamp: " + str(x))
        row.append(x)
        for j in [y for y in quoteTable.columns if y != 'DATE']:
            residue = stockDF[(stockDF['SYMBOL'] == j) & (stockDF['SERIES'] == 'EQ') & (stockDF['TIMESTAMP'] == x)]['CLOSE'].tolist()
            print("getQuoteTable found " + str(len(residue)) + " entries for symbol: " + str(j) + " with timestamp: " + str(x))
            if len(residue) == 0:
                residue = np.NaN
            else:
                residue = residue[0]
            row.append(residue)
        stockAgg.append(row)
    quoteTable = pd.DataFrame(stockAgg, columns = table_columns)
    quoteTable.fillna(quoteTable.mean(), inplace=True)
    print("getQuoteTable is saving quoteTable.csv")
    quoteTable.to_csv("quoteTable.csv", index=False, na_rep=np.NaN)
    return quoteTable

# Usage
# extractData()
# stockDF = unifyCSV(["SYMBOL", "SERIES", "TIMESTAMP", "OPEN", "HIGH", "LOW", "CLOSE"])
# qTable = getQuoteTable(["EVEREADY","EICHERMOT","SUNTV","SUNPHARMA","ASHIANA","EMAMILTD","CLNINDIA","CADILAHC","THYROCARE","BLUEDART","HINDZINC"], 
#                         stockDF)