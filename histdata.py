from bs4 import BeautifulSoup as bsoap
import re
import os
import nsepy
from os import path
import shutil
import time
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
from nsepy import get_history
from selenium.webdriver.support.ui import Select
from testscrape import scrape
from loading_data import  ext
import pandas as pd
import numpy as np
import pickle as pck
import os
from os import path
import pdb
symlist=[]
dir = '/home/sahil/projdir/fundamentals8'
lst = ext().give_file(dir,'monthly_data')
done = [i.title[0] for i in lst]
symlist=[i.title[0][0:i.title[0].find('Ltd.')] for i in 
ext().give_file(dir,'finalkfr1')]
sym =[]
for i in symlist:
    if i in done:
        continue
    else:
        sym.append(i)
r=0
symlist=sym
def mthdata(s):
  r=0
  c=0
  flag=0
  while((c < 2) & (flag!=1)):
    try:
     k = scrape(s,'m',r).scrapedata()[0][0]
     k['title'] = s
     print(type(k))
     with open('monthly_data','a+b') as d:
       pck.dump(k,d)
     flag=1
    except Exception as e:
     print(e)
     r=1
     time.sleep(7)
     c=c+1
  if(flag==1):
    with open('done_with_mth','a+b') as d:
        pck.dump(s,d)
  if(flag==1):
    print(s+' done')
for i in symlist[5:]:
  mthdata(i)
