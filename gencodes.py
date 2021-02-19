from extractcode import trading_codes
import os
os.chdir('/home/sahil/projdir')
os.system("python3 genpredict.py")
t = trading_codes()
t.set_access_code()
ac = t.get_access_code()
print(ac)
