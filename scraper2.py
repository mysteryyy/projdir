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
dir1='/home/sahil/projdir/fundamentals8'
done=[]
p = ext().give_file(dir1,'finalkfr1')
done=ext().give_file(dir1,'done_kfr')
def ff():
    from selenium.webdriver.firefox.options import Options
    options=Options()
    options.headless=True
    driver = webdriver.Firefox(options=options,executable_path='/home/sahil/Downloads/geckodriver')
    caps = DesiredCapabilities().FIREFOX
    caps["pageLoadStrategy"] = "normal"
    return driver
def cc():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox’_')
    options.add_argument('--disable-dev-shm-usage')
    driver= webdriver.Chrome('chromedriver',options=options)
    return driver
choice=sys.argv[0]
if choice=='c':
  driver=cc()
else:
  driver=ff()
stlist = pd.read_csv('/home/sahil/ind_nifty500list.csv')

os.chdir('/home/sahil/projdir')
def ext_symb(pg):
   sym = pg.find('ctag',class_='mob-hide').text.encode('ascii')
   sym = str(sym)
   bse = re.findall('\d+',sym[sym.find('BSE')+3:])
   nse = re.findall('\w+',sym[sym.find('NSE')+3:])
   return bse,nse
urls =[]
def map1(s):
  return s[0:s.find('Ltd.')-1]
def driver_act(driver):
  driver.find_element_by_link_text('Financials').click()
  return
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
lst = [map1(i) for i in stlist['Company Name'] if i not in done]
kfr=[]
last_symb=''
init_url = 'https://www.moneycontrol.com/india/stockpricequote/'
c=0
for i in lst[::-1]:
    try:
            print('in here')
            driver.get(init_url)
            print(driver.current_url)
            driver.find_element_by_xpath('//*[@id="company"]').send_keys(i)
            bt = driver.find_element_by_css_selector('div.MT2:nth-child(1) > input:nth-child(2)')
            bt.click()
            print(driver.current_url)
            ct=0
            while(1):
                if(ct>=3):
                    break
                try:
                 driver_act(driver)
                 break
                except Exception as e:
                 print(e)
                 ct=ct+1
                 time.sleep(10)
            pg1 = bsoap(driver.page_source,'html.parser')
            title = pg1.find('h1',class_='pcstname').text
            rat = pg1.find('a',title='Ratios')
            driver.get(rat['href'])
            bse,nse = ext_symb(pg1)
            flag=0
            flag1=1
            k=[]
            while(flag==0):
                try:
                    print('on')
                    url1 = driver.current_url
                    print(url1)
                    k1 = pd.read_html(url1,header=0)[0]
                    k.append(k1)
                    print(len(k1))
                    k1['title']=title
                    k1['NSE'] = ''
                    k1['BSE']=''
                    if len(bse)!=0: k1['BSE']=bse[0]
                    if len(nse)!=0: k1['NSE']=nse[0]
                    print(nse[0])
                    pg = bsoap(driver.page_source,'html.parser')
                    driver.find_element_by_css_selector('.pagination > li:nth-child(2) > a:nth-child(1)').click()
                    if(driver.current_url.encode('ascii')==url1.encode('ascii')): flag=1
                except Exception as e:
                    print(e)
                    flag1=0
                    flag=1
            if(flag1==1):
              ext().store_file(dir1,'done_kfr',i)
              k = pd.concat(k,axis=1)
              ext().store_file(dir1,'finalkfr1',k)
    except Exception as e:
             print(e)
             continue
    print(i)
    mthdata(title)
    last_symb = nse[0]
    print(nse[0])
print(c)
