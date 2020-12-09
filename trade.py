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
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
logging.basicConfig(level=logging.DEBUG)

#h = requests.get('https://api.kite.trade/margins/equity').json()
#h=pd.concat([pd.DataFrame(i,index=[j]) for i,j in zip(h,range(len(h)))])
#
# Initialise
apikey="y931xfwky24zn2l5"
apisecret="*********"
in1 = pck.load(open('initials_today.pkl','rb'))
#kite = KiteConnect(api_key=apikey)

# Redirect the user to the login url obtained
# from kite.login_url(), and receive the request_token
# from the registered redirect url after the login flow.
# Once you have the request_token, obtain the access_token
# as follows.
k = pd.read_pickle('todays_prediction.pkl')
tok = list(k.tokens)
kite = pck.load(open('kite.obj','rb'))
kws = KiteTicker(apikey,in1["access_token"])
tck=[]
tq=0
r1=kite.margins()['equity']['net']
def stream():
    global tq
    global r1
    global k
    tq=0
    def qcalc(tr,marg,open,div=len(k),r1=r1):
      global tq  
      q = round((2*r1)/(abs(tr)*div*open))
      print(q)
      tq+= (q*open)*marg
      if(tq>r1):
            q = 0
      return q

    def on_ticks(ws, ticks):
        # Callback to receive ticks.
        #logging.debug("Ticks: {}".format(ticks))
        global tck
        global k
        tck = ticks
        orderid=[]
        for i in ticks:
            k1 = k[k.tokens==i['instrument_token']]
            sl = k1.psl.values[0] if k1.prediction.values[0]>0 else k1.nsl.values[0]
            trans= kite.TRANSACTION_TYPE_BUY  if k1.prediction.values[0]>0 else kite.TRANSACTION_TYPE_SELL
            m = k1.margins.values[0]
            quant=int(qcalc(sl,m,i['last_price']))
            print(quant)
            tried=0
            tick=k1.tick.values[0]
            slp =round((abs(sl)/100)*i['last_price'],2) 
            trig = i['last_price']-slp if k1.prediction.values[0]>0 else i['last_price']+slp
            trig = trig-trig%tick
            while(tried<3):
                try:
                    order_id1=kite.place_order(tradingsymbol=k1.Symbol.values[0],exchange=kite.EXCHANGE_NSE,transaction_type=trans,
                    quantity=quant,order_type = kite.ORDER_TYPE_MARKET,variety=kite.VARIETY_CO,
                    product=kite.PRODUCT_MIS,trigger_price=trig)
                    orderid.append(order_id1)
                    break
                except Exception as e:
                    print(e)
                    tried = tried+1

        if(os.path.exists('/home/sahil/projdir/orderid.npy')):
           os.remove('/home/sahil/projdir/orderid.npy')
        np.save('orderid.npy',np.array(orderid))
        ws.stop()
    def on_connect(ws, response):
        # Callback on successful connect.
        # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
        global tok
        ws.subscribe(tok)

        # Set RELIANCE to tick in `full` mode.
        ws.set_mode(ws.MODE_FULL,tok)

    def on_close(ws, code, reason):
        # On connection close stop the event loop.
        # Reconnection will not happen after executing `ws.stop()`
        ws.stop()

    # Assign the callbacks.
    kws.on_ticks = on_ticks
    kws.on_connect = on_connect
    kws.on_close = on_close

    # Infinite loop on the main thread. Nothing after this will run.
    # You have to use the pre-defined callbacks to manage subscriptions.
    kws.connect()
stream()
