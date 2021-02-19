from datetime import datetime,timedelta
import datetime
#from bs4 import BeautifulSoup as bsoap
import re
import os
os.chdir('/home/sahil/projdir')
from os import path
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
import numpy as np
import pickle as pck
import sys
from kiteconnect import KiteConnect
import logging
from kiteconnect import KiteTicker
from extractcode import trading_codes
import pickle as pck
import sys
import requests
import investpy
import json
h = requests.get('https://api.kite.trade/margins/equity').json()
h=pd.concat([pd.DataFrame(i,index=[j]) for i,j in zip(h,range(len(h)))])

k = pd.DataFrame(columns = ['Symbol','prediction','psl','nsl','tokens','margins','tick','weights'])
k1 = pd.read_pickle('/home/sahil/projdir/instrumentdetails.pkl')
def datestring(dt):
    day=dt.date().day
    month=dt.date().month
    year=dt.date().year
    strdate = str(day)+'/'+str(month)+'/'+str(year)
    return strdate
def getprice(symb):
    today = datestring(datetime.datetime.now())
    startday = datestring(datetime.datetime.now()-timedelta(days=5))
    k1=investpy.search_quotes(text=symb,products=['stocks'],countries=['India'],n_results=2)[0].retrieve_historical_data(from_date=startday,to_date=today)
    price = k1.Close.iloc[-1]
    return price,k1
    #
def gen_pred_file(symb,psl,nsl,pred,marg,w):
    global k
    global kcheck
    info=dict()
    k11 = k1[k1.tradingsymbol==symb]
    info['Symbol'] = symb
    info['price'],kcheck = getprice(symb)
    info['prediction'] = pred
    info['tokens']= k11.instrument_token.values[0]
    info['tick'] = k11.tick_size.values[0]
    info['psl'] = psl
    info['nsl'] = nsl
    info['margins'] = h[h.tradingsymbol==symb].mis_margin.values[0]/100 
    info['weights'] = w
    if (len(k11.exchange.values)>1):
      info['exchange'] = k11.exchange.values[1]
    else:
      info['exchange'] = k11.exchange.values[0]
    print(info)
    k = k.append(info,ignore_index=True)
    return k
k=gen_pred_file('AARTIIND',2,-1,-1,.1,1)
filepath='/home/sahil/projdir/todays_prediction.pkl'
if (os.path.exists(filepath)):
    os.remove(filepath)
    k.to_pickle(filepath)
else:
    k.to_pickle(filepath)




