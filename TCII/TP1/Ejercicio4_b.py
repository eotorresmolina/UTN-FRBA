# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 20:33:57 2020

@author: Emmanuel
"""


from splane import pzmap, bodePlot
from scipy.signal import TransferFunction as tf
import matplotlib.pyplot as plt

Rb = 2000
Ra = 5*Rb
R = 1000   
C = 1e-6


K = -1/5
w0 = 1/(R*C)
qq = 1/3;

NUM = [-1, w0/qq, -1*(w0**2)]
DEN = [5*1, 5*(w0/qq), 5*(w0**2)]

my_tf = tf( NUM, DEN )

bodePlot(my_tf)
pzmap (my_tf)
