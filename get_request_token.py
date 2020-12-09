from datetime import datetime
import datetime
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
from kiteconnect import KiteConnect
import pickle as pck
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
import os

driver = webdriver.Chrome('/usr/bin/chromedriver',options=options)
apikey='*******'
apisecret='*********'
kite = KiteConnect(api_key=apikey)
driver.get(kite.login_url())
driver.implicitly_wait(6)
username = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input')
password = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input')
username.send_keys('ZF9648')
password.send_keys('sahilcrick007')
driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[4]/button').click()
pin = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/input')
pin.send_keys('118307')

driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[3]/button').click()
time.sleep(5)
request_token=driver.current_url.split('request_token=')[0]
kite = KiteConnect(api_key=apikey)
data = kite.generate_session(request_token, api_secret=apisecret)
init_tod = {'date':datetime.datetime.now().date(),'access_token':data['access_token']}
f = open('initials_today.pkl','wb')
pck.dump(init_tod,f)
f.close()
