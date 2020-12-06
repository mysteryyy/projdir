import math
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
import datetime
from datetime import date
import pandas as pd
import numpy as np
import pickle as pck
import os
import re
from  loading_data import ext
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import  confusion_matrix,accuracy_score
from sklearn.model_selection import  train_test_split
from sklearn.decomposition import PCA
from trainauto2 import neural
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense,BatchNormalization,Dropout
from keras.metrics import binary_accuracy
import pdb
et = ext()
k1=et.give_file('/home/sahil/projdir/fundamentals8','monthly_data')
k=et.give_file('/home/sahil/projdir/fundamentals8','financials_quarterly')
kk=[]
kk1=[]
ss = pd.read_csv('/home/sahil/projdir/fundamentals8/11ylatest.csv')
symbols_nse = ss.Symbol.unique()
allsym = [j.title[0] for j in k1]
def prepro(kp):
  print(kp.columns)
  kp['yearly'] = (kp.Close-kp.Close.shift(12))/kp.Close.shift(12)
  kp['quarterly'] = (kp.Close-kp.Close.shift(4))/kp.Close.shift(4)
  return kp

def prepro1(k):
  tit = k.title[0]
  tit = tit[0:tit.find('Ltd.')-1]+' '
  nse = k['NSE'].tolist()[0]
  bse=k['BSE'].tolist()[0]
  k = k.drop(['NSE','BSE','title'],axis=1)
  k = k.drop([i for i in k.columns 
  if i.find('Unnamed')!=-1],axis=1)
  knew=dict()
  if(tit in allsym):
   ret_k = [j for j in k1 if str(j.title[0])==tit][0]
  else:
    print('not found')
    return
  for i in k.columns:
    if(len(re.findall('\w{3,4}\s\'\d{2}',i))!=0):
        yr = i.split(" '")
        if(yr[0] in ['Jun','Jul']):
            if(yr[0]=='Jun'):
                yr[0]='June'
            else:
                yr[0]='July'
        yrst = yr[0]+' '+'20'+yr[1]
        print(ret_k.Date[0]==yrst)
        print(ret_k.Date[0])
        print(yrst)
        print(yrst in  list(ret_k.Date))
        k[yrst] = k[i]
        k = k.drop(i,axis=1)
        ln=[]
        try:
            ln = len(list(ret_k[pd.to_datetime(ret_k.Date)==pd.to_datetime(yrst)].quarterly))
        except:
            continue
        if(ln!=0):
         print('oh yeahhh')
         knew[yrst] = list(ret_k[pd.to_datetime(ret_k.Date)==pd.to_datetime(yrst)].quarterly)[0]
         print(list(ret_k[pd.to_datetime(ret_k.Date)==pd.to_datetime(yrst)].quarterly)[0])
        else:
         knew[yrst] = np.nan
  
  k = k.T
  k.columns = k.iloc[0]
  k = k.iloc[1:]
  try:
   k['returns'] = knew.values()
  except:
   return k
  del_cols = ['Liquidity Ratios','Profitability Ratios','Retention Ratios',
  'Valuation Ratios','EXPENDITURE']
  k = k.drop([i for i in k.columns if i in del_cols],axis=1)
  k['NSE']=nse
  k['BSE']=bse
  k['title']=tit
  return k
k1 = [prepro(i) for i in k1]
kk1=[prepro1(i) for i in k[1:]]
x=[]
def disc(l):
  g = round(l/abs(l+0.0002),0)
  return (g+1)/2
def genmat(kk1):
  x.append(np.array(kk1[kk1.columns[0]]))
  for i in kk1.columns:
      if(re.search('\d{4}',i)!=None):
            x.append(np.array(kk1[i]))
  x.append(np.array(kk1['title']))
  data.append(pd.DataFrame(data=
  np.transpose(np.array(x)),columns=cols))
kk1 = pd.concat(kk1)
kk1['returns'] = disc(kk1.returns)
kk1 = kk1.reindex(columns=([i for i in kk1.columns if i not in
['BSE','NSE']]+['NSE','BSE']))
def norm1(l):
    return ((l-l.min())/(l.max()-l.min()))
cols = [i for i in kk1.columns if i not in ['returns','title',
'NSE','BSE','date']]
def norm(kk1):
    for i in cols[:-1]:
     p = kk1[i]
     kk1[i] = (p-p.min())/(p.max()-p.min())
    return kk1
kk1 = norm(kk1)
xtr=[[]]
ytr=[]
xts=[[]]
yts=[]
kk1['date'] = pd.to_datetime(kk1.index)
def extarr(start,end,kk1):
    kk1 = kk1[(kk1.date>=start)&(kk1.date<=end)]
    kk1 = kk1.fillna(0)
    x = np.array(kk1[cols])
    y = np.array(kk1.returns)
    return x,y

def decomp(x,ncomp):
 pca = PCA(n_components=ncomp)
 x = pca.fit_transform(x)
 return x,pca
xtr,ytr = extarr(datetime.date(2000,1,1),
datetime.date(2017,1,1),kk1)
xts1,yts1 = extarr(datetime.date(2017,1,1),
datetime.date(2018,1,1),kk1)
xts2,yts2 = extarr(datetime.date(2018,1,1),
datetime.date(2019,1,1),kk1)
def validprepare(x,y):
    xtr,xts,ytr,yts = train_test_split(x,y,test_size=0.3,random_state=150)
    xts1,xts2,yts1,yts2 =  train_test_split(xts,yts,test_size=0.5,random_state=150)
    return xtr,xts,ytr,yts,xts1,xts2,yts1,yts2
x,y=extarr(datetime.date(2000,1,1),datetime.date(2019,1,1),kk1)
np.save('xquarterly.npy',x)
np.save('yquarterly.npy',y)
print(len(x))
