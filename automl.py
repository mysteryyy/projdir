import os
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
# mljar-supervised package
from supervised.automl import AutoML
x = np.load("/home/sahil/projdir/fundamentals8/xada.npy")
y = np.load("/home/sahil/projdir/fundamentals8/yada.npy")
xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=.2)
automl= AutoML(mode="Compete",total_time_limit=180)
automl.fit(xtrain,ytrain)
print(accuracy_score(ytest,automl.predict(xtest)))

