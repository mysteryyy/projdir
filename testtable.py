from bs4 import BeautifulSoup
from io import StringIO
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
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import date
from nsepy import get_history
from selenium.webdriver.support.ui import Select
import pandas as pd
import numpy as np
import pickle as pck
import os
import pandas as pd
import numpy as np
import pickle as pck
import os
from os import path
os.chdir('/home/sahil/projdir')
from testscrape import scrape
def ff():
     options=Options()
     driver = webdriver.Firefox(options=options,executable_path='/home/sahil/projdir/geckodriver')
     return driver
driver =ff()
k = pd.read_csv('/home/sahil/projdir/fundamentals8/ind_nifty500list.csv')
lg = k.Symbol.unique()
nmlist=[]
for i in lg:
  k1=k[k.Symbol==i]
  if(len(k1)!=0):
   nmlist.append(list(k1[k.columns[-1]])[0])
symlist=nmlist
def dailydata(s):
    r =0
    c=0
    flag=0
    while((c < 2) & (flag!=1)):
        try:
         k = scrape(s,'d',r,driver).scrapedata()[0]
         driver.quit()
         k['title'] = s
         print(type(k))
         flag=1
        except Exception as e:
         print(e)
         r=1
         time.sleep(7)
         c=c+1
for i in symlist:
  dailydata(i)
