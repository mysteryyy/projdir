import datetime
from datetime import date, timedelta
from numpy.lib.stride_tricks import as_strided
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from sklearn.cluster import MeanShift, estimate_bandwidth
from scipy.signal import argrelextrema
from keras.models import load_model
from keras.models import Sequential
from keras.utils import to_categorical
from keras.optimizers import SGD
from keras import initializers
from keras.layers import Flatten,TimeDistributed,Dense,Activation,LSTM,Dropout,MaxPooling1D,BatchNormalization
from keras.layers import GlobalAveragePooling1D
from keras.layers import Conv1D
from keras import metrics
from keras.metrics import binary_accuracy
from  pathlib import Path
from hurst import compute_Hc, random_walk
from os import path
import shutil
import os
import pdb
class neural:
   
    def __init__(self, lb, la,tr =0.5,loss_tr =0.69,k=pd.read_csv('11ylatest.csv')):
        self.lb = lb
        self.la = la
        self.k = k
        self.tr=np.float(tr)
        self.loss_tr =np.float(loss_tr)
        self.k['date'] = pd.to_datetime(self.k.Date).apply(lambda x:x.date())
    def strided_app(self, a, L=20, S=1):  # Window len = L, Stride len/stepsize = S
        s0,s1 = a.strides
        return np.lib.stride_tricks.as_strided(a, 
shape=(len(a)-(self.lb-1), self.lb, a.shape[1]), strides=(s0,s0,s1))
    def strided_app1(self,a, L=30, S=1 ):  # Window len = L, Stride len/stepsize = S
        s0,s1 = a.strides
        return np.lib.stride_tricks.as_strided(a, shape=(len(a)-(self.lb-1),self.lb,7), strides=(s0,s0,s1))
   
    def makedf(self,temp1):
            t1 =[]
            if(len(temp1)<self.lb):
                return
            else:
                xt =  neural.strided_app(self,np.array(temp1[['Open',
                'High','Low','Close','date','ret','Symbol']]))
                
                d = neural.ardiv(self,xt)
                t = pd.DataFrame(d.reshape(len(d)*self.lb,7))
                t.columns = ['o','h','l','c','date','ret','Symbol']
                t1.append(t)
            t1 = pd.concat(t1)
            return t1
    def makedf2(self,temp1):
            t1 =[]
            if(len(temp1)<self.lb):
                return
            else:
                xt =  neural.strided_app(self,np.array(temp1[['rsi','ft','h','date','ret','Symbol']]))
                
                d = neural.ardiv2(self,xt)
                t = pd.DataFrame(d.reshape(len(d)*self.lb,6))
                t.columns = ['rsi','ft','h','date','ret','Symbol']
                t1.append(t)
            t1 = pd.concat(t1)
            return t1
    def makedf1(self,temp1):
            t1 =[]
            if(len(temp1)<self.lb):
                return
            else:
                xt =  neural.strided_app(self,np.array(temp1[['Close','ret']]))
                d = neural.ardiv1(self,xt)
                t = pd.DataFrame(d.reshape(len(d)*self.lb,2))
                t.columns = ['c','ret']
                t1.append(t)
            t1 = pd.concat(t1)
            return t1
             
            
    def norm1(r):
        print (str(r.std()))
        print(r)
        return (r/abs(r))*(r-(r.mean()-4*r.std()))/(8*r.std())
    def norm_minmax(r):
        return r.max(),r.min()
    def norm2(r):
        print (str(r.std()))
        return r.mean()+4*r.std(),r.mean()-4*r.std() 
    def norm3(r,max1,min1):
        return (r/abs(r))*(r-min1)/(max1-min1)
    def norm4(r,max1,min1):
        s = (r/(r-0.00001)).astype(int)
        return s*(r-min1)/(max1-min1)
    def makearr(self,x,y,disc):
        df = pd.DataFrame()
        df['arr'] = x
        df['ret'] = y
        if(disc):
            df['ret'] = df.ret-0.5
        df1 =df[df.ret>0]
        df2 =df[df.ret<0]
        if(len(df1)>=len(df2)):
         df1 = df1[0:len(df2)]
        else:
         df2 = df2[0:len(df1)]
        ndf = pd.concat([df1,df2])
        x = np.array(list(ndf.arr))    
        return x,np.array(ndf.ret)
    def disc(l):
        dir1 = (l/abs(l))
        return (dir1+1)/2
    def makearr1(self,x,y,yd,yh,ys):
        df = pd.DataFrame()
        df['arr'] = x
        df['ret'] = y
        df['ret'] = df.ret-0.5
        df['hurst'] = yh
        df['date'] = yd
        df['Symbol'] = ys
        df1 =df[df.ret>0]
        df2 =df[df.ret<0]
        if(len(df1)>=len(df2)):
         df1 = df1[0:len(df2)]
        else:
         df2 = df2[0:len(df1)]
        ndf = pd.concat([df1,df2])
        ndf['ret'] = neural.disc(ndf.ret)
        x = np.array(list(ndf.arr))    
        return x,np.array(ndf.ret),np.array(ndf.date),np.array(ndf.hurst),np.array(ndf.Symbol)
    
    def app(a,b):
        
        return np.append(a,b,1)
    def lm(self,xs):
      df = pd.DataFrame(data =xs, columns=['data'])
    
      n=5 # number of points to be checked before and after 
      # Find local peaks
      df['min'] = df.iloc[argrelextrema(df.data.values, np.less_equal, order=n)[0]]['data']
      df['max'] = df.iloc[argrelextrema(df.data.values, np.greater_equal, order=n)[0]]['data']
      df['data'] = df.data/list(df.data)[-1]
    
      a = argrelextrema(df.data.values, np.less_equal, order=n)
      a1 = argrelextrema(df.data.values, np.greater_equal, order=n)
      a = np.concatenate([a,a1],axis=1)
      arr = np.zeros(self.lb)
      for i in a:
        arr[i] = df.data.iloc[i]
      arr = arr.reshape(len(arr),1)
      return arr
    def attr(self,p): #function for transformation of prices into required inputs
             def h(l):
                 s = compute_Hc(l)
                 return s[0]
             k = p.dropna()
             
             k['mp'] = (k.High+k.Low)/2
             k['im'] = 1*(k.mp-(k.Low.rolling(window = 20).min()))/((k.High.rolling(window=20).max())-(k.Low.rolling(window = 20).min()))
             k['ft'] = 0.5*np.log((1+k.im)/(1-k.im))
             k['delta'] = k.Close.shift(-1)-k.Close
             k['du'] = ((k.delta/abs(k.delta)+1)/2)*k.delta#keeping only the positive k.delta
             k['dd'] = ((abs((k.delta/abs(k.delta))-1)/2))*abs(k.delta)#keeping only the negative delta
             k['rs'] = k.du.rolling(window=14).mean()/k.dd.rolling(window=14).mean()
             k['rs5'] = k.du.rolling(window=5).mean()/k.dd.rolling(window=5).mean()
             k['rsi'] = 100.0 - (100.0 / (1.0 + k.rs))
             k['rsi5'] = 100.0 - (100.0 / (1.0 + k.rs5))
             k['rsi'] = k.rsi/100
             k['rsi5'] = k.rsi5/100
             k['ft']= (k.ft-k.ft.min())/(k.ft.max()-k.ft.min())
             
             k['h'] = k.Close.rolling(150).apply(h)           
                 
             k = k.dropna()
             return k
    def ardiv(self,x):
        d  = []
        for i in range(len(x)):
            d.append(neural.app(x[i][:,[0,1,2,3]]/x[i][self.lb-1][3],x[i][:,[4,5,6]]))
        print(np.array(d).shape)
        return np.array(d)
    def ardiv2(self,x):
        d  = []
        for i in range(len(x)):
            d.append(neural.app(x[i][:,[0,1,2]],x[i][:,[3,4,5]]))
        print(np.array(d).shape)
        return np.array(d)
    def ardiv1(self,x):
        d  = []
        for i in range(len(x)):
            d.append(neural.app(neural.lm(self,x[i][:,[0]]),x[i][:,[1]]))
        print(np.array(d).shape)
        return np.array(d)
    def maketab(self,st1,st2,ch):
        t1 =[]
        t2 = []
        
        for i in self.k.Symbol.unique():
                k1 = self.k[self.k.Symbol==i]
                k1['ret'] = neural.norm1((k1.Close.shift(-self.la)-k1.Close)/k1.Close)
                k1 = k1.dropna()
                if(ch=='rsift'):
                 k1 = neural.attr(self,k1)
                 
                 temp1 =k1[(k1.date>=st1) 
                 & (k1.date<=st2)]
                 temp2 = k1[k1.date>=st2]
                 t1.append(neural.makedf2(self,temp1))
                 t2.append(neural.makedf2(self,temp2))
                 
                else:
                 temp1 =k1[(k1.date>=st1) 
                 & (k1.date<=st2)]
                 temp2 = k1[k1.date>=st2]
                 
                 if(ch=='ohlc'):
                     print(np.array(temp1[['Open','High','Low','Close']]))
                     t1.append(neural.makedf(self,temp1))
                     t2.append(neural.makedf(self,temp2))
                
                 else:
                    print(np.array(temp1[['Close']]))
                    t1.append(neural.makedf1(self,temp1))
                    t2.append(neural.makedf1(self,temp2))
                
                
        
        t1 =pd.concat(t1)
        t2 = pd.concat(t2)
        return t1,t2
    def setupdir(mkdir,t1,t2):
        p = Path('/content/drive/My Drive/'+mkdir)
        pth='/content/drive/My Drive/'+mkdir
        print('__BEFCLASSINSIDE__')
        print(t1.head(20))
        pth = os.getcwd()+"/"+mkdir
        if path.exists(p):
            shutil.rmtree(pth)
        if(p.is_dir()==False):
           os.mkdir(mkdir)
        
        os.chdir(pth)
        t1.to_pickle('inittrain.pkl')
        
        t2.to_pickle('inittest.pkl')
        print(os.getcwd())
    def genarr2(self,st1,st2):
        t1,t2 = neural.maketab(self,st1,st2,'rsift')
        mkdir ='testlogs'+'rsiftwithdate1'+str(st1)+'to'+str(st2)+'_'+str(self.lb)+'_'+str(self.la)
        neural.setupdir(mkdir,t1,t2)
        t22 = t1.copy()
            
        
        t33 = t2.copy()
        print('aft_func_check1')
        print(t33.head(20))
        print('aft_func_check')
        print(t1.head(20))
        t22.to_pickle('init_train_rsift.pkl')
        
        t33.to_pickle('init_test_rsift.pkl')
        
        x = np.array(t22[t22.drop(['date','ret','Symbol'],1).columns]).reshape(int(len(t22)/(self.lb)),self.lb,3)
        y = np.array(t22.ret.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t22)/self.lb))]])

        x1 = np.array(t33[t33.drop(['date','ret','Symbol'],1).columns]).reshape(int(len(t33)/self.lb),self.lb,3)
        yd1 = np.array(t33.date.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t33)/(self.lb)))]])
        ys1 = np.array(t33.Symbol.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t33)/(self.lb)))]])

        yh1 = np.array(t33.h.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t33)/(self.lb)))]])
        yd = np.array(t22.date.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t22)/(self.lb)))]])
        ys = np.array(t22.Symbol.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t22)/(self.lb)))]])

        yh = np.array(t22.h.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t22)/(self.lb)))]])
        y1 = np.array(t33.ret.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t33)/(self.lb)))]])
        x,y = neural.makearr(self,list(x),list(y),False)
        
        return x,y,yh,x1,y1,yh1,yd,yd1,ys,ys1
    def genarr(self,st1,st2):
            t1,t2 = neural.maketab(self,st1,st2,'ohlc')
            mkdir ='testlogs'+str(st1)+'to'+str(st2)+'_'+str(self.lb)+'_'+str(self.la)
            neural.setupdir(mkdir,t1,t2)
            norms = list(t1[t1.drop(
            ['date','ret','Symbol'],1).columns].apply(neural.norm_minmax))
            def trans(p):
                cols =['o','h','l','c']
                j=0
                for i in range(len(cols)):
                    
                    p[cols[i]] = neural.norm4(p[cols[i]],norms[i][0],norms[i][1])
                    j=j+2
                return p
            
            
            
            t1 = trans(t1)
            t22 = t1.copy()
            
            t2 = trans(t2)
            t33 = t2.copy()
            print('aft_func_check1')
            print(t33.head(20))
            print('aft_func_check')
            print(t1.head(20))
            t22.to_pickle('init_train_ohlc.pkl')
            
            t33.to_pickle('init_test_ohlc.pkl')
            
            
            x1 = np.array(t33[t33.drop(['date','ret','Symbol'],1).columns]).reshape(int(len(t33)/self.lb),self.lb,4)
            ymm = np.array(t33.date.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t33)/(self.lb)))]])
            yd = np.array(t22.date.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t22)/(self.lb)))]])
            ys = np.array(t22.Symbol.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t22)/(self.lb)))]])
            yd1 = np.array(t33.date.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t33)/(self.lb)))]])
            ys1 = np.array(t33.Symbol.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t33)/(self.lb)))]])
            y1 = np.array(t33.ret.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t33)/(self.lb)))]])
            yh = np.array(t22.h.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t22)/(self.lb)))]])
            yh1 = np.array(t33.h.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t33)/(self.lb)))]])
            x = np.array(t22[t22.drop(['date','ret','Symbol'],1).columns]).reshape(int(len(t22)/(self.lb)),self.lb,4)
            y = np.array(t22.ret.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t22)/self.lb))]])
            x,y,yd,yh,ys = neural.makearr1(self,list(x),list(y),list(yd),
            list(yh),list(ys))
            y1 = np.array(neural.disc(pd.Series(y1)))
            return x,y,yh,x1,y1,yh1,yd,yd1,ys,ys1
            
    def genarr1(self,st1,st2,ch):
            t1,t2 = neural.maketab(self,st1,st2,'c')
            mkdir ='testlogs'+str(st1)+'to'+str(st2)+'_'+str(self.lb)+'_'+str(self.la)
            p = Path('/content/drive/My Drive/'+mkdir)
            pth='/content/drive/My Drive/'+mkdir

            pth = os.getcwd()+"/"+mkdir
            if(p.is_dir()==False):
               os.mkdir(mkdir)
            
            os.chdir(pth)
            print(os.getcwd())

           
            t11 = t1[['c','ret']]
            if(ch=='sparse'):
              norm = neural.norm2(t11[t11.c!=0].c)
            else:
              norm = neural.norm2(t11.c)

                
                
            
            
            
            t1['c'] = neural.norm4(t1['c'],norm[0],norm[1])

            t2['c'] = neural.norm4(t2['c'],norm[0],norm[1])
            t1.to_pickle('init_train_c_'+ch+'.pkl')
            
            t2.to_pickle('init_test_c_'+ch+'.pkl')
            t3=t2
            x1 = np.array(t3['c']).reshape(int(len(t3)/self.lb),self.lb,1)
            np.array(t3.date.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t3)/(self.lb)))]])
            y1 = np.array(t3.ret.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t3)/(self.lb)))]])
            x = np.array(t1['c']).reshape(int(len(t1)/(self.lb)),self.lb,1)
            y = np.array(t1.ret.iloc[[((self.lb*(i+1))-1) for i in range(int(len(t1)/self.lb))]])
            x,y = neural.makearr(self,list(x),list(y))
            
            return x,y,x1,y1,ymm
    def trainproc(self,x,y,yh,yd,x1,y1,yh1,yd1,ys,ys1,ch,history,model):
        p=False
        acc2 =[]
        acc3 = []
        md =[]
        lss=[]
        c=0
        c1=0
        def accm(lta,ltb,ydd,yhh,yss):
         y11 = []
         y2= []
         pr1= model.predict(lta)
         for i in pr1:
            y11.append(i)
         for i in ltb:
            y2.append(i)
         print('trainacc')
         df = pd.DataFrame({'real':y2,'predicted':y11})
         print(df)
         print('dfcreated')
         print(ydd)
         print(len(df))
         print(len(ydd))
         df['date']=ydd
         print('datedone')
         df['check'] = df.real*df.predicted
         print('checkdone')
         df['hurst'] = yhh
         print('hurstdonw')
         df['Symbol'] = yss
         print('symboldone')
         df1 = df[df.hurst>0.53]
         
         print('without hurst ',len(df[df.check>0])/(len(df)))
         print('with hurst ',len(df1[df1.check>0])/(len(df1)))
         print(len(df1))
         
         return df,df1
        def acc_bin(x1,y1,tr):
            ypred =[i[1] for i in model.predict(x1)]
            yreal = [np.argmax(i) for i in y1]
            df =pd.DataFrame()
            df['real'] = yreal
            df['predicted'] = ypred
            df1 = df[(df.predicted>tr) | (df.predicted<1-tr)]
            df1['pred'] = df1.predicted.apply(lambda x:1 if x>tr else 0)
            return len(df1[df1.real==df1.pred])/len(df1),len(df1)/len(df)
            
        
        while(True):
                testdf = pd.DataFrame()
                if(history.history['loss'][-1]<self.loss_tr):
                 

                  nm = str(20) + '_init_ '+str(c)+'.h5'
                  model.save(nm)
                  md.append(nm)
                  lss.append(history.history['loss'][-1])
                  testdf['model name'] = md
                  testdf['final loss'] = lss
                  score, accz = model.evaluate(x1, y1,
                            batch_size=350)
                  tr_acc,ret_rat= acc_bin(x1,y1,self.tr)
                  testdf['threshold accuracy'] = tr_acc
                  testdf['retention ratio'] = ret_rat

                  if(ch=='sparse'):
                   nm = 'conv_'+'elliot'+str(self.lb)+'_'+str(self.la)+'_testdetails.csv'
                  else:
                   nm = 'mlplstm_'+str(self.lb)+'_'+str(self.la)+'_testdetails.csv'

                  if path.exists(nm):
                    os.remove(nm)
                  testdf.to_csv(nm)
                  c = c+1
                  history= model.fit(x,y, epochs =3 ,verbose = 1,batch_size= 350)

                  
            
                
                if(c>600):
                    break
                else:
                     history= model.fit(x,y, epochs =3 ,verbose = 1,batch_size= 350)
                     c1 = c1+1
                     if(c1>5000):
                         break
        if(p):
            print('qualified')
        else:
            print('not qualified')
        testdf['model name'] = md
        testdf['final loss'] = lss
        testdf['accuracy'] = acc   
    def mlplstm(self,x,y,yh,yd,x1,y1,yh1,yd1,ys,ys1,ch,epoch):
        y=to_categorical(y)
        y1=to_categorical(y1)
        def modelz():
            model = Sequential()
            model.add(BatchNormalization(input_shape=(20,x.shape[1])))
            model.add(TimeDistributed(Dense(15,activation='tanh'), input_shape=(20, 4)))
            model.add(BatchNormalization())
            model.add(Dropout(0.2))
            model.add(TimeDistributed(Dense(5,activation = 'tanh')))
            model.add(BatchNormalization())
            model.add(TimeDistributed(Flatten()))
            model.add(LSTM(32, input_shape=(20, 2),return_sequences=True))
            model.add(BatchNormalization())
            model.add(Dropout(0.4))
            model.add(LSTM(16,activation='relu'))
            model.add(BatchNormalization())
            model.add(Dropout(0.4))
            model.add(Dense(16,activation='relu'))
            model.add(Dense(2,activation='softmax'))
            model.compile(loss='binary_crossentropy',optimizer = 'adam',metrics=['accuracy'])
            history = model.fit(x,y,validation_data=(x1,y1),epochs =epoch ,verbose = 1,batch_size= 350,shuffle=True)
            return history,model
        history,model=modelz()
        print('here')
        neural.trainproc(self,x,y,yh,yd,x1,y1,yh1,yd1,ys,ys1,ch,history,model)
        np.save('xmlplstm.npy',x)
        np.save('x1mlplstm.npy',x1)
        np.save('y1mlplstm.npy',y1)
        np.save('ymlplstn.npy',y)
         

    def conv(self,x,y,yh,yd,x1,y1,yh1,yd1,ys,ys1,ch): 
        p=False
        model = Sequential()
        print('reached')
        model.add(Conv1D(64,(3,),input_shape=(x.shape[1],x.shape[2]),activation='tanh'))
        model.add(Conv1D(64, (3,), activation='tanh'))
        if(ch=='sparse'):
            model.add(MaxPooling1D(pool_size=(2,)))
        model.add(Dropout(0.25))
        model.add(Conv1D(32, (3,), activation='tanh'))
        model.add(Conv1D(32, (3,), activation='tanh'))
       
        model.add(GlobalAveragePooling1D())
        model.add(Dropout(0.25))
        
        
        model.add(Dense(128, activation='tanh'))
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='tanh'))
        
        model.compile(loss='mean_squared_error', optimizer='adam')
        history=model.fit(x,y, epochs =40 ,verbose = 1,batch_size= 150,shuffle=True)
        neural.trainproc(x,y,yh,yd,x1,y1,yh1,yd1,ys,ys1,ch,history,model)
        np.save('x.npy',x)
        np.save('x1.npy',x1)
        np.save('y1.npy',y1)
        np.save('y.npy',y)
                    
