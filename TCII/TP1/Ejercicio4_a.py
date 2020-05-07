# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 20:33:57 2020

@author: Emmanuel
"""


from splane import pzmap, bodePlot
from scipy.signal import TransferFunction as tf
import matplotlib.pyplot as plt

R1 = 2000
R2 = R1
R3 = 1000   
C = 1e-6

wc = 1 / (R3*C)

NUM = [0, 1, -wc]
DEN = [0, 1, wc]

my_tf = tf( NUM, DEN )

bodePlot(my_tf)
pzmap (my_tf)
