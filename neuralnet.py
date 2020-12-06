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
from sklearn.feature_selection  import SelectKBest, chi2
from sklearn.ensemble import AdaBoostClassifier
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
os.chdir('/home/sahil/projdir/fundamentals8')
x=np.load('xquarterly.npy')
y=np.load('yquarterly.npy')
def validprepare(x,y):
    xtr,xts,ytr,yts = train_test_split(x,y,test_size=0.3,random_state=5)
    xts1,xts2,yts1,yts2 =  train_test_split(xts,yts,test_size=0.5,random_state=5)
    return xtr,xts,ytr,yts,xts1,xts2,yts1,yts2
def discr(y):
 y = y/abs(y)
 return (y+1)/2
xtr,xts,ytr,yts,xts1,xts2,yts1,yts2 = validprepare(x,y)
xtr,ytr = neural(1,1).makearr3(xtr.tolist(),ytr.tolist(),True,'normal',0.85,0.1)
def prepro_mixup(ytr):
    ytr3 =[]
    for i in ytr:
      ytr3.append(np.array(i))
    return np.array(ytr3)
ytr = prepro_mixup(ytr)
def themodel(x):
    model = Sequential()
    model.add(BatchNormalization(input_shape=(x.shape[1],)))
    model.add(Dropout(0.2))
    model.add(Dense(60, input_dim=62, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    model.add(Dense(45, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.3))
    model.add(Dense(2, activation='softmax'))
    model.compile(loss='kullback_leibler_divergence', 
    optimizer='adam', metrics=['accuracy'])
    return model
def to_cat(ytr):
    ytr = to_categorical(ytr)
    return ytr
def conf_mat(xts1,yts1,model):
    tn,fp,fn,tp = confusion_matrix([np.argmax(i) for i in yts1],
    [np.argmax(i) for i in model.predict(xts1)]).ravel()
    return tn,fp,fn,tp
def train_params(xtr,ytr,xts1,yts1,model,l):
 losshist=[]
 modelname=[]
 strength=[]
 for i in range(l):
  history=model.fit(xtr,ytr,validation_data=(xts1,yts1),epochs=1,verbose=1,batch_size=40)
  losshist.append(history.history['val_accuracy'][-1])
  modelname.append(model)
  tn,fp,fn,tp = conf_mat(xts1,yts1,model)
  pr = tp/(tp+fp)
  rc = tp/(tp+fn)
  f1 = 2*pr*rc/(pr+rc)
  strength.append(f1+model.evaluate(xts1,yts1)[1])
 df=pd.DataFrame()
 df['model'] = modelname
 df['valacc']=losshist
 df['strength'] = strength
 return df
model=themodel(xtr)
yts = to_categorical(yts)
yts1=to_categorical(yts1)
yts2 = to_categorical(yts2)
def nn():
    df =train_params(xtr,ytr,xts1,yts1,model,100)
    tn,fp,fn,tp = conf_mat(xts2,yts2,
    list(df[df.strength==df.strength.max()].model)[0])
    return tn,fp,fn,tp
tn,fp,fn,tp=nn()
dfz = []
df=pd.DataFrame()
with open('modelrecords','rb') as f:
 dfz = pck.load(f)
df['model_type'] = ['neuralnet']
df['preprocessing_type'] = ['normal_quarterly']
df['accuracy'] = [model.evaluate(xts2,yts2)[1]]
pr = tp/(tp+fp)
rc = tp/(tp+fn)
f1 = 2*pr*rc/(pr+rc)
df['strength'] = [f1+df.accuracy[0]]
print(df.strength)
dfz = dfz.append(df)
with open('modelrecords','wb') as f:
 pck.dump(dfz,f)
