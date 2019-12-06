import fire
from urllib.request import urlopen, Request

def download(url):
    file_name = url.split('/')[-1]
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    uR = Request(url, headers=headers)
    u = urlopen(uR).read()
    f = open(file_name, 'wb')
    f.write(u)
    f.close()

def getStocks(dr, mr, yr):
    start_date = dr[0]; end_date = dr[1]
    start_month = mr[0]; end_month = mr[1]
    start_year = yr[0]; end_year = yr[1]

    dmonth={1:'JAN',2:'FEB',3:'MAR',4:'APR',5:'MAY',6:'JUN',7:'JUL',8:'AUG',9:'SEP',10:'OCT',11:'NOV',12:'DEC'}

    for y in range(start_year, end_year + 1):
        for m in range(start_month, end_month + 1):
            for d in range(start_date, end_date + 1):
                print("Fetching info for: ", y, m, d)
                try:
                    if d < 10:
                        print("https://www.nseindia.com/content/historical/EQUITIES/"+str(y)+"/"+dmonth[m]+"/cm0"+str(d)+dmonth[m]+str(y)+"bhav.csv.zip")
                        download_pb("https://www.nseindia.com/content/historical/EQUITIES/"+str(y)+"/"+dmonth[m]+"/cm0"+str(d)+dmonth[m]+str(y)+"bhav.csv.zip")
                    else:
                        print("https://www.nseindia.com/content/historical/EQUITIES/"+str(y)+"/"+dmonth[m]+"/cm"+str(d)+dmonth[m]+str(y)+"bhav.csv.zip")
                        download_pb("https://www.nseindia.com/content/historical/EQUITIES/"+str(y)+"/"+dmonth[m]+"/cm"+str(d)+dmonth[m]+str(y)+"bhav.csv.zip")
                except:
                    continue
    
