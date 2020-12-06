from bs4 import BeautifulSoup as bsoap
import re
import os
from os import path
import shutil
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
import numpy as np
import pickle as pck
from loading_data import ext
import sys
dir1='/home/sahil/projdir/fundamentals8'
def scrape_fin():
 os.system('python /home/sahil/projdir/scraper2.py')
 yield
def download_data():
 os.system('python /home/sahil/projdir/histdata.py')
 yield
print(sys.argv[0])
