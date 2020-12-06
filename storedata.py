from bs4 import BeautifulSoup as bsoap
import re
import os
from os import path
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
import numpy as np
import pickle as pck
from loading_data import ext
from testscrape import scrape
import sys
import investpy
import itertools
dir1='/home/sahil/projdir/'
dir2=dir1+'fundamentals8/'
transf = neural(20,10)
k = pd.read_csv(dir2+'ind_nifty500list.csv')
k1 = pd.read_csv(dir1+'11ylatest.csv')
lg = k1.Symbol.unique()
nmlist=[]
symb=[]
for i in lg:
  
  k11=k[k.Symbol==i]
  if((len(k11)!=0)):
   nmlist.append(list(k11[k.columns[-1]])[0])
   symb.append(i)
dir3 = dir1+'daily_price_data'
os.chdir(dir3)
tot = []
for (i,j) in itertools.zip_longest(nmlist,symb):
    try:
        df = investpy.search(text=i)[0].retrieve_historical_data('01/01/2002','25/04/2020')
        df['Symbol'] = j 
        tot.append(df)
    except Exception as e:
        print(e)
        print(j+' not done')
        continue
    print(j+' done')
df1 = pd.concat(tot)
df1.to_pickle(dir1+'dailydata.pkl')

