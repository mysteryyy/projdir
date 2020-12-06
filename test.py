import os
import pickle as pck
import sys
from loading_data import ext
os.system('docker build . -t scrape')
os.system('docker volume create data4')
os.system('docker run scrape')
