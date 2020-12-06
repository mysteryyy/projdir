from bs4 import BeautifulSoup as bsoap
import re
import os
from os import path
import shutil
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from nsepy import get_history
from datetime import date
import pandas as pd
import numpy as np
import pickle as pck
import os
import re
os.chdir('/home/sahil/fundamentals8')
k=[]
s = []
def ext_symb(k):
   df = k
   return k['NSE'][0]
def ext_df(k,i):
   if(k['NSE'][0]==i):
      return k
def ext_by_symb(i):
    print(i)
    df_st = map(ext_df,k,i)
    return df_st

def conc_df(prev,curr):
    return prev['NSE'][0]==curr['NSE'][0]

    
k1=[]
prev=pd.DataFrame()

with open('key_financial_ratios','rb') as f:
  try:
      while True:
        curr =  pck.load(f)
        if(len(prev!=0)):
            if(conc_df(prev,curr)):
                df = pd.concat([prev,curr],axis=1,join='inner')
                df = df.loc[:,~df.columns.duplicated()]
                curr=df
                k= k[:-1]
                k.append(df)
            else:
                k.append(curr)
        else:
            k.append(curr)
        prev = curr

             
  except EOFError:
        pass
s = pd.Series(map(ext_symb,k))
