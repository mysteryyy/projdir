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
import datetime
from  datetime import timedelta
import investpy
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
kite = KiteConnect(api_key=apikey)

# Redirect the user to the login url obtained
# from kite.login_url(), and receive the request_token
# from the registered redirect url after the login flow.
# Once you have the request_token, obtain the access_token
# as follows.

k = pd.read_pickle('todays_prediction.pkl')
price = k.price.iloc[-1]
tok = list(k.tokens)
kite = pck.load(open('kite.obj','rb'))
kws = KiteTicker(apikey,in1["access_token"])
tck=[]
tq=0
r1=kite.margins()['equity']['net']/6
order_id = kite.place_order(
        variety=kite.VARIETY_REGULAR,
        exchange=kite.EXCHANGE_NSE,
        tradingsymbol="ZEEL",
        transaction_type=kite.TRANSACTION_TYPE_BUY,
        quantity=1,
        product=kite.PRODUCT_MIS,
        order_type=kite.ORDER_TYPE_MARKET
    )

def stream():
    global tq
    global r1
    global k
    tq=0
    def qcalc(tr,marg,open,w,r1=r1):
      global tq  
      q = round((4*w*r1)/(abs(tr)*open))
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
            if(i['last_price']<=price):
                print("exiting because there is no gap")
                sys.exit()
            k1 = k[k.tokens==i['instrument_token']]
            #sl = k1.psl.values[0] if k1.prediction.values[0]>0 else k1.nsl.values[0]
            trans= kite.TRANSACTION_TYPE_BUY  if k1.prediction.values[0]>0 else kite.TRANSACTION_TYPE_SELL
            trans_close =kite.TRANSACTION_TYPE_SELL if k1.prediction.values[0]>0 else kite.TRANSACTION_TYPE_BUY
 
            if(k1.exchange.values[0]=='BSE'):
                exch = kite.EXCHANGE_BSE
            else:
                exch = kite.EXCHANGE_NSE

            sl = k1.nsl.values[0]
            tp = k1.psl.values[0]
            m = k1.margins.values[0]
            quant=int(qcalc(sl,m,i['last_price'],k1.weights.values[0]))
            print(quant)
            tried=0
            tick=k1.tick.values[0]
            slp =round((abs(sl)/100)*i['last_price'],2) 
            tpp =round((abs(tp)/100)*i['last_price'],2) 
            tpp=tpp-tpp%tick
            trigsl = i['last_price']-slp if k1.prediction.values[0]>0 else i['last_price']+slp
            trigtp = i['last_price']+tpp if k1.prediction.values[0]>0 else i['last_price']-tpp
            trigtp = trigtp-trigtp%tick
            print('take profit ',trigtp)
            trigsl = trigsl-trigsl%tick
            trigsl=round(trigsl,2)
            print('stop loss ',trigsl)
            while(tried<3):

                try:
                    #Entry Order
                    ##Cover order
                    #order_id1=kite.place_order(tradingsymbol=k1.Symbol.values[0],exchange=exch,transaction_type=trans,
                    #    quantity=quant,order_type = kite.ORDER_TYPE_MARKET,variety=kite.VARIETY_CO,
                    #product=kite.PRODUCT_MIS,trigger_price=trigsl)
                    ##
                    order_id1=kite.place_order(tradingsymbol=k1.Symbol.values[0],exchange=exch,transaction_type=trans,
                        quantity=quant,order_type = kite.ORDER_TYPE_MARKET,variety=kite.VARIETY_REGULAR,
                    product=kite.PRODUCT_MIS)

                    #Exit Orders
                    try:
                        order_id2=kite.place_order(tradingsymbol=k1.Symbol.values[0],exchange=exch,transaction_type=trans_close,
                        quantity=quant,order_type = kite.ORDER_TYPE_SLM,variety=kite.VARIETY_REGULAR,
                        product=kite.PRODUCT_MIS,trigger_price=trigsl,validity=kite.VALIDITY_DAY)
                    except Exception as e:
                        os.system('python3 exitorder.py')
                    order_id3=kite.place_order(tradingsymbol=k1.Symbol.values[0],exchange=exch,transaction_type=trans_close,
                    quantity=quant,order_type = kite.ORDER_TYPE_LIMIT,variety=kite.VARIETY_REGULAR,
                    product=kite.PRODUCT_MIS,price=trigtp)
#
#
#
                    
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
