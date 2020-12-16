from kiteconnect import KiteConnect
import numpy as np
import pandas as pd
import pickle as pck
import os
os.chdir('/home/sahil/projdir')
order = np.load('orderid.npy')
kite = pck.load(open('kite.obj','rb'))
for i in kite.orders():
    try:  
        kite.exit_order(variety=kite.VARIETY_CO,order_id=i['order_id'],parent_order_id = i['parent_order_id'])
    except Exception as e:
        print(e)
