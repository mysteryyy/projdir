import datetime
import networkx as nx
import requests
from datetime import timedelta
from bs4 import BeautifulSoup as bsoap
import re
import os
os.chdir('/home/sahil/projdir')
from os import path
import shutil
import time
from networkx.algorithms import tree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from keras.models import load_model
import pandas as pd
import numpy as np
import pickle as pck
from loading_data import ext
from testscrape import scrape
import sys
import investpy
import itertools
from trainauto3 import neural
dir1='/home/sahil/projdir/'
dir2=dir1+'fundamentals8/'
k =pd.read_pickle('dailydata.pkl')
inst = pd.read_pickle('instrumentdetails.pkl')
transf = neural(20,10)
smlist = k.Symbol.unique()
mod = load_model('predictmodel.h5')
pred=[]
sym=[]
vol=[]
price=[]
psl=[]
nsl=[]
def sl(k1):
    
    k1 = k1.tail(30)
    a = k1.ret
    a = a.sort_values()
    a = a.reset_index(drop=True)
    d = []
    for i in a:
      dist =  ((i-a)**2).sum()/len(a)
      dist =1/(1+dist**0.5)
      d.append(dist)
    
    d = pd.Series(d,index=a)
    err=[]
    def cdf1(x):
       return len(a[a>x])/(len(a))
    def cdf2(x):
      return len(a[a<x])/(len(a))
    def mom(x):
      s = (a[a>x]*d[d.index>x].values).sum()/len(d)
      return s
    def mom1(x):
      s = (a[a<x]*-1*d[d.index<x].values).sum()/len(d)
      return s
    def p2(x):
       return x*-1*(1-cdf2(x))+mom1(x)
    def p(x):
      return x*(1-cdf1(x))+mom(x)
    vals =[]
    vals1=[]
    for i in np.arange(-4,0,0.1):
      vals.append(p(i))
    for i in np.arange(0,4,0.1):
      vals1.append(p2(i))

    s = pd.DataFrame()
    s1 = pd.DataFrame()

    s['ret'] = np.arange(-4,0,0.1)
    s1['ret'] = np.arange(0,4,0.1)
    s1['p'] = vals1
    s['p'] = vals
    neg = s1[abs(s1.p)==abs(s1.p).min()].ret.reset_index(drop=True)[0]
    pos = s[abs(s.p)==abs(s.p).min()].ret.reset_index(drop=True)[0]
    return pos,neg
def date_to_str(dt):
    return '0'+str(dt.day) if dt.day<10 else str(dt.day),'0'+str(dt.month) if dt.month<10 else str(dt.month),str(dt.year)
preddf =[] 
s1=0
corrdf=pd.DataFrame()
for i in smlist:
    try:
        di,mi,yi = date_to_str(datetime.datetime.now().date()-timedelta(days=380))
        df11,mf,yf = date_to_str(datetime.datetime.now().date())
        df = investpy.search(text=i)[0].retrieve_historical_data('01/01/2018',df11+'/'+mf+'/'+yf)
        df['Symbol'] = i 
        print(df)
        df = transf.attr(df)
        print(df)
        df['ret'] = ((df.Close-df.Open)/df.Open)*100
        dfcor = df
        dfcor = dfcor.tail(50)
        dfcor[i] = df.ret
        corrdf=pd.concat([corrdf,dfcor[i]],axis=1)
        corrdf = corrdf.fillna(method='ffill')
        print(corrdf.corr(method='pearson'))
        df['vol_range'] = abs(df.Close-df.Open)/(df.High-df.Low)
        df['volrange']  = df.vol_range.rolling(window=20).mean()
        df1 = df.tail(20)
        xt = np.array(df1[['rsi','rsi5','ft','h']])
        xt = xt.reshape(1,20,4)
        pred=mod.predict(xt)[0][1]-mod.predict(xt)[0][0]
        sym = i
        volrange = df.volrange.values[-1]
        vol = list(df.Volume)[-1]
        price = list(df.Close)[-1]
        pos,neg=sl(df)
        psl = pos
        nsl=neg
        s1 =s1+1
        preddf1 = pd.DataFrame({'Symbol':sym,'prediction':pred,'Volume':vol,'price':price,'psl':psl,'nsl':nsl,'volrange':volrange},index=[s1])
        preddf.append(preddf1)
    except Exception as e:
        print(e)
        print(i+' not done')
        continue
    print(i+' done')
h = requests.get('https://api.kite.trade/margins/equity').json()
h=pd.concat([pd.DataFrame(i,index=[j]) for i,j in zip(h,range(len(h)))])
preddf = pd.concat(preddf)     
preddf = preddf.sort_values(by='Volume',ascending=False)
preddf = preddf.head(25)
preddf = preddf.sort_values(by='price')
preddf = preddf.head(22)
preddf = preddf.sort_values(by='volrange')
preddf = preddf.head(16)
preddf = preddf.sort_values(by='prediction',ascending=False)
#preddf = preddf.tail(3).append(preddf.iloc[3:6])
cr = corrdf[list(preddf.Symbol.values)].corr(method='pearson')
cr1 = abs(cr)
def valtrans(cr1):
    for i in cr1.columns:
        predval=preddf[preddf.Symbol==i].prediction.values[0]
        cr1[i] = 0.4*1/abs(predval)+0.6*cr1[i]
    return cr1
cr1=valtrans(cr1)
g = nx.from_numpy_matrix(np.matrix(cr1))
d = dict()
for i in range(len(cr.columns)):
    d[i] = cr.columns[i]
g = nx.relabel_nodes(g,mapping=d)
stocks=tree.minimum_spanning_tree(g)
stocks = sorted(stocks.edges())
st=[]
for i in range(len(stocks)-1):
    st1 = list(set(stocks[i]+stocks[i+1]))
    st = list(set(st+st1))
    if(len(st)>=6):
        break
stocks=st
preddf = pd.concat([preddf[preddf.Symbol==i] for i in stocks])
preddf = preddf.sort_values(by='price')
tq=0
r1=6000
def qcalc(r1,tr,open,div=len(preddf)):
  global tq  
  q = round((2*r1)/(abs(tr)*div*open))
  tq+= q*open
  if(tq>10*r1):
        q = 0
  return q
quant=[]
marg=[]
for date,i in preddf.iterrows():
  quant.append(qcalc(r1,i.psl,i.price) if  i.prediction>0  else qcalc(r1,i.nsl,i.price))
if(os.path.exists('/home/sahil/projdir/todays_prediction.pkl')):
  os.remove('/home/sahil/projdir/todays_prediction.pkl')
token=[]
tck=[]
for index,row in preddf.iterrows():
   token.append(list(inst[inst.tradingsymbol==row['Symbol']].instrument_token)[0])
   marg.append(list(h[h.tradingsymbol==row['Symbol']].mis_margin)[0]/100)
   tck.append(inst[inst.tradingsymbol==row['Symbol']].tick_size.values[0])
preddf['tokens'] = token
preddf['margins'] = marg
preddf['tick'] = tck
preddf.to_pickle('todays_prediction.pkl')
