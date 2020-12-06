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
apikey='*********'
apisecret='*********'
kite = KiteConnect(api_key=apikey)
print(kite.login_url())
request_token=input("request toke: ")
data = kite.generate_session(request_token, api_secret=apisecret)

