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
import sys
from kiteconnect import KiteConnect
import pickle as pck
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='/usr/share/app/.env')
driver = webdriver.Chrome('/usr/bin/chromedriver',options=options)
apikey=os.getenv("APIKEY")
apisecret=os.getenv("APISECRET")
passw=os.getenv("PASS")
pin1=os.getenv("PIN")
driver.get('https://developers.kite.trade/login')
email_xpath='//*[@id="id_email"]'
em=driver.find_element_by_xpath(email_xpath)
em.send_keys('yishusahil@gmail.com')
passw_xpath = '//*[@id="id_password"]'
pa = driver.find_element_by_xpath(passw_xpath)
pa.send_keys(passw)
driver.find_element_by_xpath('//*[@id="main"]/div/form/p[3]/input').click()

kite = KiteConnect(api_key=apikey)
driver.get(kite.login_url())
driver.implicitly_wait(6)
username = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[1]/input')
password = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input')
username.send_keys('ZF9648')
password.send_keys(passw)
driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[4]/button').click()
pin = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/input')
pin.send_keys(pin1)

driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[3]/button').click()
time.sleep(5)
print(driver.current_url)
request_token=driver.current_url.split('request_token=')[1].split('&')[0]
print(request_token)
kite = KiteConnect(api_key=apikey)
data = kite.generate_session(request_token, api_secret=apisecret)
if(os.path.exists('/home/sahil/projdir/kite.obj')):
    print('deleting...')
    os.remove('/home/sahil/projdir/kite.obj')
pck.dump(kite,open('kite.obj','wb'))
kite.set_access_token(data["access_token"])
init_tod = {'date':datetime.datetime.now().date(),'access_token':data["access_token"],'request_token':request_token}
f = pck.dump(init_tod,open('initials_today.pkl','wb'))
