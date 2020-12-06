import os
import pickle as pck
class ext:
    def __init__(self):
        
        pass
    def give_file(self,dir_loc,filename):
        k =[]
        os.chdir(dir_loc)
        with open(filename,'rb') as f:
            try:
                while True:
                    k.append(pck.load(f,encoding='latin1'))
            except:
                    pass
        return k
    
    def store_file(self,dir_loc,filename,k):
        os.chdir(dir_loc)
        with open(filename,'a+b') as f:
         pck.dump(k,f)
    
    def convert_file(self,dir_loc,filename):
        os.chdir(dir_loc)
        pck1 = ext.give_file(self,dir_loc,filename)
        os.remove(filename)
        for i in pck1:
            with open(filename,'a+b') as f:
             pck.dump(i,f)

        os.chdir('/home/sahil')

