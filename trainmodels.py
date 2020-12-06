import os
from os import path
import shutil
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from nsepy import get_history
import datetime
from datetime import date
import pandas as pd
import numpy as np
import pickle as pck
import os
import re
from  loading_data import ext
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import  confusion_matrix,accuracy_score
from sklearn.model_selection import  train_test_split
from sklearn.decomposition import PCA
from trainauto2 import neural
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense,BatchNormalization,Dropout
from keras.metrics import binary_accuracy
import pdb
import pickle as pck
os.chdir('/home/sahil/projdir')
import pandas as pd
import numpy as np
import warnings
import os
import datetime
warnings.filterwarnings("ignore")
from keras.models  import load_model
from keras.losses  import binary_crossentropy
from keras.models  import Sequential
from keras.optimizers  import SGD
from keras import  initializers
from keras.layers  import Flatten,Dense,TimeDistributed,Activation,LSTM,Dropout
import os
import time
import os
import numpy as np
import pandas as pd
import datetime
from trainauto3  import neural
f = neural(20,10)
x,y,yh,x1,y1,yh1,yd,yd1,ys,ys1=f.genarr2(datetime.date(2008,1,1),datetime.date(2018,6,1))
f.mlplstm(x,y,yh,yd,x1,y1,yh1,yd1,ys,ys1,'ok',100)

