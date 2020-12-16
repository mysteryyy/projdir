import scipy
import matplotlib.pyplot as plt
import vegas
from scipy.integrate import nquad
from scipy.stats import t,norm
from scipy.special import gamma
from scipy.integrate import dblquad,tplquad,quad
import numpy as np
from numpy.random import normal,uniform
al=.55
nu=4.52
s=1.72
u=0.02
lim=20
minret = t.rvs(nu,u/(720),s/(720**al),size=720)
print(np.cumsum(minret).min())
print(np.cumsum(minret).max())
print(np.cumsum(minret)[-1])
