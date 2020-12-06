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
def_dir='/home/sahil/projdir/fundamentals8'
os.chdir(def_dir)
k = pd.read_pickle('combined_balance_sheet1.pkl')
def del_bs(k):
 k['dca'] = k.ca-k.ca.shift(-1)
 k = k.dropna()
 k['dcash'] = k.cash-k.cash.shift(-1)
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
 k['accrual'] = (k.dca-k.dcash)-(k.dcl-k.dstd-k.dtp)
 k = k.dropna()
 k['incomp'] = k['Total Income From Operations']/k.ata
 k = k.dropna()
 k['acccomp'] = k.accrual/k.ata
 k = k.dropna()
 k['cashcomp'] = k.incomp-k.acccomp
 k = k.dropna()
 return k
f3 = k
f3['std1'] = f3['std']
f3 =f3.dropna()
nums = [i for i in f3.columns if i not in ['title','date']]
f3[nums] = f3[nums].apply(
lambda x:pd.to_numeric(x,errors='coerce'))
f3 = f3.dropna()
ftot=[]
for i in f3.title.unique():
  ftot.append(del_bs(f3[f3.title==i]))
f3 = pd.concat(ftot)
