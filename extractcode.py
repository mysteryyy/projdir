import os
import pickle as pck
import sys
import pandas as pd

class trading_codes:

    def __init__(self):
       pass
       os.system('docker build . -t scrape')
    
    def set_access_code(self):
       os.system('docker volume create data4')
       os.system('docker run -v data4:/usr/share/app scrape')
    def get_access_code(self):
       dir_loc = '/var/lib/docker/volumes/data4/_data'
       k = pck.load(open(dir_loc+'/initials_today.pkl','rb')) 
       data = pck.load(open(dir_loc+'/kite.obj','rb')) 
       if(os.path.exists('/home/sahil/projdir/kite.obj')):
           os.remove('/home/sahil/projdir/kite.obj')
       if(os.path.exists('/home/sahil/projdir/initials_today.pkl')):
           os.remove('/home/sahil/projdir/initials_today.pkl')
       os.system('mv '+dir_loc+'/initials_today.pkl /home/sahil/projdir/')
       os.system('mv '+dir_loc+'/kite.obj /home/sahil/projdir/')
       os.system('docker volume prune -f')
       os.chdir('/home/sahil/projdir')
       os.system('docker system prune -f')
       os.system('docker volume rm data4')
       return k,data


