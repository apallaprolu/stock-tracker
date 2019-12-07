import fire
import requests

def download(url):
    file_name = url.split('/')[-1]
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    uR = requests.get(url, timeout=100, headers=headers)
    f = open(file_name, 'wb')
    f.write(uR.content)
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
                        print("Processing request: https://www.nseindia.com/content/historical/EQUITIES/"+str(y)+"/"+dmonth[m]+"/cm0"+str(d)+dmonth[m]+str(y)+"bhav.csv.zip")
                        download("https://www.nseindia.com/content/historical/EQUITIES/"+str(y)+"/"+dmonth[m]+"/cm0"+str(d)+dmonth[m]+str(y)+"bhav.csv.zip")
                    else:
                        print("Processing request: https://www.nseindia.com/content/historical/EQUITIES/"+str(y)+"/"+dmonth[m]+"/cm"+str(d)+dmonth[m]+str(y)+"bhav.csv.zip")
                        download("https://www.nseindia.com/content/historical/EQUITIES/"+str(y)+"/"+dmonth[m]+"/cm"+str(d)+dmonth[m]+str(y)+"bhav.csv.zip")
                except:
                    print("No data found for: ", y, m, d)
                    continue

if __name__ == '__main__':
    fire.Fire(getStocks)