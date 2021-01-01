from datetime import datetime
import datetime
#from bs4 import BeautifulSoup as bsoap
import re
import os
os.chdir('/home/sahil/projdir')
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
import logging
from kiteconnect import KiteTicker
from extractcode import trading_codes
import pickle as pck
import sys
import requests
import json
k = pd.DataFrame(columns = ['Symbol','prediction','psl','nsl','tokens','margins','tick'])
k1 = pd.read_pickle('/home/sahil/projdir/instrumentdetails.pkl')
def gen_pred_file(symb,psl,nsl,pred):
    global k
    info=dict()
    info['Symbol'] = symb
    info['prediction'] = pred
    info['tokens']= k1[k1.tradingsymbol==symb].instrument_token.values[0]
    info['tick'] = k1[k1.tradingsymbol==symb].tick_size.values[0]
    info['psl'] = psl
    info['nsl'] = nsl






