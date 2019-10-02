import csv, time, lxml, json, requests
import pandas as pd
from pandas.io.json import json_normalize
from datetime import datetime
import bs4 as bs
import urllib3 as urllib
from plotly import graph_objs as go
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def jsontodataframe(): #collect OHLC data from scstrade

    companies = {'Habib Bank Limited':'HBL','Engro Chemical':'ENGRO'} #just need to add code here to get more data values
    url = 'http://www.scstrade.com/stockscreening/SS_CompanySnapShotHP.aspx/chart'

    payload = {"date1":"01/01/2010","date2":"06/01/2019","rows":20,"page":1,"sidx":"trading_Date",
    "sord":"desc"}
    
    data = []
    for company in companies:
        payload["par"] = companies[company] # this is equivalent to the ticker name (different every iteration)
        print(payload)
        json_data = requests.post(url, json=payload).json() #download the json POST request from scstrade
        json_normalize(json_data)
        
        df = pd.DataFrame(json_data) #convert the json to pandas dataframe
        df = pd.io.json.json_normalize(json_data['d'], errors='ignore')
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Change'] #rename the columns to better names

        df['Date'] = df['Date'].str.strip('/Date()')
        df['Date'] = pd.to_datetime(df['Date'], origin='unix', unit='ms') #convert unix timestamp to pandas datetime and set the index
        df['Date'] = df['Date'].dt.floor('d') # return only dates
        
        df['ID'] = companies[company]
        df.set_index(['ID'], inplace=True)
        data.append(df)
        
    return pd.concat(data).to_csv('OHLC_values.csv')


def visualize_candlestick():
     df = pd.read_csv("OHLC_values.csv")
     fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                 open=df['Open'],
                 high=df['High'],
                 low=df['Low'],
                 close=df['Close'])])

     fig.show()     

def visualize_barchart(): 
    #so far this function is really simple but doing this with
    #multiple par ID's and switching between them will be slightly tricky
    df = pd.read_csv("OHLC_values.csv")
    plt.bar(df['Date'], df['Change'], align='center', alpha=0.5)
    plt.title('Date and Change in Stock Price')
    plt.ylabel('Change')
    plt.xlabel('Date')
    plt.show()
