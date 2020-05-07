# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 22:30:54 2020

@author: Emmanuel
"""


from splane import bodePlot, pzmap
from scipy.signal import TransferFunction as tf
import matplotlib.pyplot as plt
import math

R = 2.12* (10**6)
C2 = 4700e-12
C5 = 47e-12

w0 = 1/ (math.sqrt(R*R*C2*C5))
qq = 10 / 3

NUM = [-w0**2]
DEN = [1, w0/qq, w0**2]

my_tf = tf( NUM, DEN )

bodePlot(my_tf)
pzmap(my_tf)


    