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
b = et.give_file('/home/sahil/projdir/fundamentals8','balance_sheet')
f = et.give_file('/home/sahil/projdir/fundamentals8','financials_quarterly')
m = et.give_file('/home/sahil/projdir/fundamentals8','monthly_data')
def prepro(kp):
  print(kp.columns)
  kp['yearly'] = (kp.Close-kp.Close.shift(12))/kp.Close.shift(12)
  kp['quarterly'] = (kp.Close-kp.Close.shift(4))/kp.Close.shift(4)
  return kp
def badcols(k):
    bad_col=[]
    for l in k.columns:
        s1 = re.findall('\w{3,4}',l)
        s2 = re.findall('\d{2}',l)
        if(len(s1)!=0 and len(s2)!=0):
            try:
              pd.to_datetime(s1[0]+'20'+s2[0]).date()
            except:
               bad_col.append(l)

        else:
          bad_col.append(l)
    return bad_col
def trans_date(l):
   s1 = re.findall('\w{3,4}',l)
   s2 = re.findall('\d{2}',l)
   if(len(s1)!=0 and len(s2)!=0):
     try:
      return pd.to_datetime(s1[0]+'20'+s2[0]).date()
     except:
      return l
   else:
     return l
def conv_month_col(k):
   print(k.Date[0])
   print(k.title[0])
   try:
    k['date'] = k.Date.apply(lambda x:pd.to_datetime(x).date())
   except:
    return pd.DataFrame(columns=k.columns)
   k = prepro(k)
   return k
def conv_col(k):
    tit = k.title[0]
    tit = tit[0:tit.find('Ltd.')-1]+' '
    k['title'] = tit
    print(k.title[0])
    bad_col=badcols(k)
    temp = k[bad_col[1:]]
    k.index = k[k.columns[0]]
    k = k.drop(bad_col,axis=1) 
    k = k.T
    k['date'] = [trans_date(i) for i in k.index]
    for i in temp.columns:
      k[i] = temp[i][0]
    return k
def del_bs(k):
 k['dca'] = k.ca-k.ca.shift(-1)
 k = k.dropna()
 k['dc'] = k.cash-k.cash.shift(-1)
 k = k.dropna()
 k['dcl'] = k.cl-k.cl.shift(-1)
 k = k.dropna()
 k['dstd'] = k.std1-k.std1.shift(-1)
 k = k.dropna()
 k['dtp'] = k.tp - k.tp.shift(-1)
 k = k.dropna()
 k['ta'] = k['Total Assets']
 k = k.dropna()
 k['ata'] = (k.ta+k.ta.shift(-1))/2
 k = k.dropna()
 k['accrual'] = (k.dca-k.dc)-(k.dcl-k.dstd-k.dtp)-k.depreciat
 k = k.dropna()
 k['incomp'] = k['Total Income From Operations']/k.ata
 k = k.dropna()
 k['acccomp'] = k.accrual/k.ata
 k = k.dropna()
 k['cashcomp'] = k.incomp-k.acccomp
 k = k.dropna()
 return k
def prep_data(f,b,m):
    transcol=[conv_col(i) for i in f]
    f = pd.concat(transcol)
    b = pd.concat([conv_col(i) for i in b])
    m = pd.concat([conv_month_col(i) for i in m])
    valid_col = [i for i in b.columns if pd.isnull(i)==False]
    b = b[valid_col]
    return f,b,m
def conv_ind(sym):
 k1 = k[k.Symbol==sym].Industry.get_values()
 if(len(k1)==1):
  return k1[0]
 else:
  return np.nan
 
f = pd.read_pickle('/home/sahil/projdir/fundamentals8/modified_financials_quarterly.pkl')
b = pd.read_pickle('/home/sahil/projdir/fundamentals8/modified_balance_sheet.pkl')
m = pd.read_pickle('/home/sahil/projdir/fundamentals8/modified_monthly_data.pkl')
f1 = f.merge(b,on=['date','NSE'])
f1['title'] = f1.title_x
f2 = m[['yearly','date','title']].merge(f1,on=['date','title'])
ac = pd.read_pickle('/home/sahil/projdir/fundamentals8/accrual.pkl')
f3 =pd.DataFrame()
f3['NSE'] = f2['NSE']
f3['ca'] = f2['Total Current Assets']
f3['cash'] = f2['Cash And Cash Equivalents']
f3['cl'] = f2['Total Current Liabilities']
f3['std1'] = f2['Short Term Borrowings']
f3['tp'] = f2['Deferred Tax Liabilities [Net]']
f3['Total Assets'] = f2['Total Assets']
f3['Total Income From Operations'] = f2['Total Income From Operations']
f3['depreciat'] = f2['depreciat']
not_nums = ['NSE','yearly','date','title']
for i in not_nums:
 f3[i] = f2[i]
nums = [i for i in f3.columns if i not in not_nums]
f3[nums] = f3[nums].apply(
lambda x:pd.to_numeric(x,errors='coerce'))
f3 = f3.dropna()
f3 = pd.concat([del_bs(f3[f3.title==i]) for i in 
f3.title.unique()])
k = pd.read_csv('ind_nifty500list.csv')
f3['Industry'] = f3.NSE.apply(conv_ind)
f3 = f3.dropna()
yea=0
tot=0
for i in f3.date.unique():
   f4 = f3[f3.date==i]
   for j in f4.Industry.unique():
       f41 = f4[f4.Industry==j]
       f41 = f41.sort_values(by=['cashcomp'])
       f5 = f41.tail(round(0.1*len(f41)))
       yea = yea+len(f5[f5.yearly>0])
       tot = tot+len(f5)
def prepro2(k):
    tit = k.title[0]
    tit1 = tit[0:tit.find('Ltd.')-1]+' '
    [i for i in md if i.title[0]==tit1][0]
def  prepro1(k):
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
