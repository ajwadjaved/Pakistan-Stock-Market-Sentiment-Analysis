import csv, time, lxml, json, requests
import pandas as pd
from pandas.io.json import json_normalize
import bs4 as bs
import urllib3 as urllib
import matplotlib.pyplot as plt
%matplotlib inline

def get_urls():
    Base_url = "http://www.scstrade.com"
 
    # Build a dictionary of companies and their abbreviated names 
    companies = {'Habib Bank Limited':'HBL', 'Engro Chemical':'ENGRO'}

    # Create a list of the news section urls of the respective companies 
    return ['http://www.scstrade.com/stockscreening/SS_CompanySnapShot.aspx?symbol={}'.format(v) 
                for k,v in companies.items()]

def jsontodataframe(): #collect OHLC data from scstrade

    url = 'http://www.scstrade.com/stockscreening/SS_CompanySnapShotHP.aspx/chart'

    payload = {"par":"HBL","date1":"01/01/2019","date2":"06/01/2019","rows":20,"page":1,"sidx":"trading_Date",
    "sord":"desc"}

    json_data = requests.post(url, json=payload).json() #download the json POST request from scstrade
    json_normalize(json_data)
    df = pd.DataFrame(json_data) #convert the json to pandas dataframe

    df = pd.io.json.json_normalize(json_data['d'], errors='ignore')

    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Change'] #rename the columns to better names

    df['Date'] = df['Date'].str.strip('/Date()')
    df['Date'] = pd.to_datetime(df['Date'], origin='unix', unit='ms') #convert unix timestamp to pandas datetime and set the index
    df.set_index(['Date'], inplace=True)
    df.to_csv("/home/duke/PSMSA/SCSTrade/OHLC_values.csv") #save .csv file for later usage


def visualizedata():
    df = pd.read_csv("/home/duke/PSMSA/SCSTrade/OHLC_values.csv)
