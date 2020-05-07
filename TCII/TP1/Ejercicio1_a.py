# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
@autor: Torres Molina Emmanuel

"""
from splane import pzmap, bodePlot
from scipy.signal import TransferFunction as tf
import matplotlib.pyplot as plt

R1 = 10**3
R2 = 2.7 * (10**6)
R3 = R1
R4 = 1000

K = -1 / (R1*R4)

NUM = [0, 0, -((R3*R4) + (R2*R4) + (R2*R3))]
DEN = [0, 0, R1*R4]

my_tf = tf(NUM, DEN)

bodePlot(my_tf)