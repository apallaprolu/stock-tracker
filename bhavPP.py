# Post-process BhavCopy ZIPs and create a final CSV of per company share variation across all days.
# You need to run this wherever the .csv.zip files are present if you are running this standalone.

import glob, os
import re
import pandas as pd
import zipfile
from dateutil.parser import parse

dmonth={1:'JAN',2:'FEB',3:'MAR',4:'APR',5:'MAY',6:'JUN',7:'JUL',8:'AUG',9:'SEP',10:'OCT',11:'NOV',12:'DEC'}

os.chdir("./")

date_regex = re.compile('^cm(\d{2})([a-zA-Z]{3})(\d{4})(.*)')

columns_to_extract = ["SYMBOL", "TIMESTAMP", "OPEN", "HIGH", "LOW", "CLOSE" ]
stocks = pd.DataFrame(columns = columns_to_extract)
database = {}

# We need to unzip each guy and read atleast one CSV for the dataframe.


for file in glob.glob("*.zip"):
    # day = date_regex.match(file).group(1)
    # month = date_regex.match(file).group(2)
    # year = date_regex.match(file).group(3)
    print("Extracting " + file)
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall("./")
    print("Deleting " + file)
    os.remove(file)

for file in glob.glob("*.csv"):
    tmp = pd.read_csv(file)
    print("Processing: " + file)
    stocks = stocks.append(tmp[columns_to_extract])

LOS = list(set(stocks['SYMBOL'].tolist()))

for sym in LOS:
    print("Processing data for " + str(sym))
    tmp = stocks[stocks['SYMBOL'] == sym]
    tmp['TIMESTAMP'] = tmp['TIMESTAMP'].apply(lambda x: parse(x))
    tmp.sort_values('TIMESTAMP')
    database[sym] = []
    for index, row in tmp.iterrows():
        database[sym].append(row['CLOSE'])







        
    

