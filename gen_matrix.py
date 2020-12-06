import pdb
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
from sklearn.ensemble import AdaBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
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
base_dir='/home/sahil/projdir/fundamentals8'
et = ext()
simcolpairs = np.load(base_dir+'/simcolpairs.npy') 
knift = pd.read_csv(base_dir+'/ind_nifty500list.csv')
k1=et.give_file(base_dir,'monthly_data')
k=et.give_file(base_dir,'finalkfr1')
kk=[]
kk1=[]
ss = pd.read_csv('/home/sahil/projdir/fundamentals8/11ylatest.csv')
symbols_nse = ss.Symbol.unique()
allsym = [j.title[0] for j in k1]
kk1 = pd.read_pickle(base_dir+'/financials_yearly.pkl')
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
  knew[k.columns[0]] = 'returns'
  if(tit in allsym):
   ret_k = [j for j in k1 if str(j.title[0])==tit][0]
  else:
    print('not found')
    return
  for i in k.columns:
    if(len(re.findall('\w{3,4}\s\d{2}',i))!=0):
        yr = i.split(' ')
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
        ln = len(list(ret_k[ret_k.Date==yrst].quarterly))
        if(ln!=0):
         knew[yrst] = list(ret_k[ret_k.Date==yrst].quarterly)[0]
        else:
         knew[yrst] = np.nan
  
  k = k.append(knew,ignore_index=True)
  k = k.set_index(k.columns[0])
  k = k.T
  del_cols = ['Liquidity Ratios','Profitability Ratios','Retention Ratios',
  'Valuation Ratios','Key Performance Ratios']
  k = k.drop([i for i in k.columns if i in del_cols],axis=1)
  k['NSE']=nse
  k['BSE']=bse
  k['title']=tit
  return k
def disc(l):
  g = l/abs(l)
  return (g+1)/2
def exc_col(k,simcolpairs):
  for i in simcolpairs:
     c1 = i[0]
     c2 = i[1]
     l1 = k[c1]
     k[c1].fillna(k[c2],inplace=True)
     k[c2].fillna(l1,inplace=True)
     k = k.drop(c2,1)
  return k
def gen_financials(k,k1):
    k1=[prepro(i) for i in k1]
    kk1=[prepro1(i) for i in k[1:]]
    kk1 = pd.concat(kk1)
    kk1['ret1']=kk1.returns
    kk1['returns'] = disc(kk1.returns)
    kk1 = kk1.reindex(columns=([i for i in kk1.columns if i not in
    ['BSE','NSE']]+['NSE','BSE']))
    return kk1
kk1=gen_financials(k,k1)
kk1 = exc_col(kk1,simcolpairs)
kk1 = kk1.dropna(axis=1,how='all')
kk1['date'] = pd.to_datetime(kk1.index)
def genmat(kk1):
  x.append(np.array(kk1[kk1.columns[0]]))
  for i in kk1.columns:
      if(re.search('\d{4}',i)!=None):
            x.append(np.array(kk1[i]))
  x.append(np.array(kk1['title']))
  data.append(pd.DataFrame(data=
  np.transpose(np.array(x)),columns=cols))
def norm1(l):
    return ((l-l.min())/(l.max()-l.min()))

cols = [i for i in kk1.columns if i not in ['Industry','returns','title','NSE','BSE','ret1','date']]

def norm(kk1):
    for i in cols[:-1]:
     p = kk1[i]
     kk1[i] = (p-p.min())/(p.max()-p.min())
    return kk1
xtr=[[]]
ytr=[]
xts=[[]]
yts=[]
def conv_ind(sym):
 k1 = knift[knift.Symbol==sym].Industry.get_values()
 if(len(k1)==1):
  return k1[0]
 else:
  return np.nan
def industry_norm(kk1):
    kk1['Industry']=kk1.NSE.apply(conv_ind)
    kkcomb=[]
    for i in kk1.Industry.unique():
     kk1temp  = norm(kk1[kk1.Industry==i])
     kkcomb.append(kk1temp)
    kk1 = pd.concat(kkcomb)
    kk1 = kk1.dropna(axis=1,how='all')
    kk1 = kk1.fillna(0)
    cols = [i for i in kk1.columns if i not in ['Industry','returns','title','NSE','BSE','date','ret1']]
    kk1['date'] = kk1.date.apply(lambda x:x.date())
    return kk1
kk1=industry_norm(kk1)
kk1.to_pickle('industrynorm_fundamentals.pkl')
#kqcomb=[]
#for i in kk1.date.unique():
#  ktemp = kk1[kk1.date==i]
#  mret = ktemp.ret1.mean()
#  for j in ktemp.NSE.unique():
#    ktempsym = ktemp[ktemp.NSE==j]
#    ktempsym['ret2'] = ktempsym.ret1-mret
#    kqcomb.append(ktempsym)
#kk1 = pd.concat(kqcomb)  
#kk1['ret2'] = norm1(kk1.ret1)
def extarr(start,end,kk1):
    kk11 = kk1[(kk1.date>=start)&(kk1.date<=end)]
    kk11 = kk11.fillna(0)
    x = np.array(kk11[cols])
    y = np.array(kk11['returns'])
    return x,y


x,y = extarr(datetime.date(2000,1,1),
datetime.date(2020,1,1),kk1)
xtr,xts,ytr,yts = train_test_split(x,y,test_size=0.3)
tr = DecisionTreeClassifier(max_depth=3)
clf = AdaBoostClassifier(base_estimator=tr,n_estimators=250,random_state=50,learning_rate=1.0)
clf.fit(xtr,ytr)
tn,fp,fn,tp=confusion_matrix(yts,clf.predict(xts)).ravel()
print((tp*tn-fp*fn)/((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))**0.5)
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
