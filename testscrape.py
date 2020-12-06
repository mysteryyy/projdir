from bs4 import BeautifulSoup as bsoap
import re
import os
import nsepy
from os import path
import shutil
import time
import datetime
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
from loading_data import ext
import pandas as pd
import numpy as np
import pickle as pck
import os
class scrape:
    def __init__(self,name,ch,ch1):
      self.name=name
      self.ch=ch
      self.ch1=ch1
    def scrapedata(self):
        


        os.chdir('/home/sahil/projdir/fundamentals8')
        caps = DesiredCapabilities().FIREFOX
        if(self.ch1==0):
          caps["pageLoadStrategy"] = "eager"
        else:
          caps["pageLoadStrategy"] = "normal"
        options=Options()
        options.headless=True

        driver = webdriver.Firefox(options=options,executable_path='/home/sahil/Downloads/geckodriver')
        driver.get('https://www.moneycontrol.com/india/stockpricequote/')
        print(driver.current_url)
        tbox = driver.find_element_by_xpath('//*[@id="company"]')
        tbox.send_keys(self.name)
        btxpath =  "div.MT2:nth-child(1) > input:nth-child(2)"
        flag=0
        c=0
        while(flag==0):
            try:
             driver.find_element_by_css_selector(btxpath).click()
             flag=1
            except Exception as e:
             print(e)
             c=c+1
             if(c==3): 
                flag=1
             print('sleeping')
             time.sleep(5)
        print(driver.current_url)
        hpxpath= "Historical Prices"
        flag=0
        c=0
        while(flag==0):
            try:
             driver.find_element_by_link_text(hpxpath).click()
             flag=1
            except Exception as e:
             print(e)
             c=c+1
             print('sleeping')
             if(c==3):
                flag=1
             time.sleep(5)
        pg = bsoap(driver.page_source,'html.parser')
        driver.get(pg.find('a',title='Click Here')['href'])
        nse1 = Select(driver.find_element_by_css_selector('#ex'))
        if(self.ch=='d'):
            nse1.select_by_visible_text('NSE')
            nse = Select(driver.find_element_by_name('frm_dy'))
            nse.select_by_visible_text('01')
            nse = Select(driver.find_element_by_name('frm_mth'))
            nse.select_by_visible_text('Mar')
            nse = Select(driver.find_element_by_name('frm_yr'))
            nse.select_by_visible_text('2008')
            nse = Select(driver.find_element_by_name('to_dy'))
            nse.select_by_visible_text('01')
            nse = Select(driver.find_element_by_name('to_mth'))
            nse.select_by_visible_text('Mar')
            nse = Select(driver.find_element_by_name('to_yr'))
            nse.select_by_visible_text('2019')
            p = driver.find_element_by_css_selector('td.PL20:nth-child(1) > form:nth-child(1) > div:nth-child(4) > input:nth-child(4)')
            p.click()
        else:
            nse =Select(driver.find_element_by_name('mth_frm_mth'))
            nse.select_by_visible_text('Mar')
            nse =Select(driver.find_element_by_name('mth_frm_yr'))
            nse.select_by_visible_text('2000')
            nse =Select(driver.find_element_by_name('mth_to_mth'))
            nse.select_by_visible_text('Mar')
            nse =Select(driver.find_element_by_name('mth_to_yr'))
            nse.select_by_visible_text('2019')
            p = driver.find_element_by_css_selector('td.PT15:nth-child(3) > form:nth-child(1) > div:nth-child(4) > input:nth-child(3)')
            p.click()


        k=[]
        while(True):
            pg = bsoap(driver.page_source,'html.parser')

            tab = pg.find('table',class_='tblchart')
            k.append(pd.read_html(str(tab)))
            url = str(driver.current_url.encode('ascii'))
            url = url[0:url.find('?')]
            elem = pg.find_all('a',class_='nextprev')
            if(len(elem)==0):
                break
            url1 = elem[0]['href'].encode('ascii')
            url = url+url1
            driver.get(url)
            print('next')
        print(k)
        driver.quit()
        return k

