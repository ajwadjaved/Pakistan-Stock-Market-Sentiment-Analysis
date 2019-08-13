import csv, time, lxml, json, requests, json
import pandas as pd
from pandas.io.json import json_normalize
import bs4 as bs
import urllib3 as urllib

#Base_url = "http://www.pkfinance.info"
# 
## Build a dictionary of companies and their abbreviated names 
#companies = {'Habib Bank Limited':'HBL', 'Engro Chemical':'ENGRO'}
#             
## Create a list of the news section urls of the respective companies 
#url_list = ['https://pkfinance.info/kse/stock/{}?tb=true'.format(v) for k,v in companies.items()]
#print(url_list)

url = 'http://www.scstrade.com/stockscreening/SS_CompanySnapShotHP.aspx/chart'
payload = {"par":"HBL","date1":"01/01/2019","date2":"06/01/2019","rows":20,"page":1,"sidx":"trading_Date","sord":"desc"}

json_data = requests.post(url, json=payload).json()

json_normalize(json_data)
df = pd.DataFrame(json_data)

df = pd.io.json.json_normalize(json_data['d'], errors='ignore')

df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Change']
#df.set_index(['Date'], inplace=True)

df['Date'] = df['Date'].str.strip('/Date()')
#df['Date'] = pd.to_datetime(df['Date'], format='%d%m%Y')
df['Date'] = pd.to_datetime(df['Date'], origin='unix', unit='ms')