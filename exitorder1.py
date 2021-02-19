from kiteconnect import KiteConnect
import numpy as np
import pandas as pd
import pickle as pck
import os
os.chdir('/home/sahil/projdir')
order = np.load('orderid.npy')
kite = pck.load(open('kite.obj','rb'))
p=kite.positions()
l=len(p['net'])
for i in range(l):
   p1=p['net'][i]
   q=abs(p1['quantity'])
   if(q==0):
       continue
   sym=p1['tradingsymbol']
   order_id = kite.place_order(
        variety=kite.VARIETY_REGULAR,
        exchange=kite.EXCHANGE_NSE,
        tradingsymbol=sym,
        transaction_type=kite.TRANSACTION_TYPE_BUY,
        quantity=q,
        product=kite.PRODUCT_MIS,
        order_type=kite.ORDER_TYPE_MARKET
    )


   
