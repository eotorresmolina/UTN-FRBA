# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 19:52:14 2020

@author: Emmanuel Torres Molina
"""

"""
Ejercicio 1_a del TP2 de Teoría de los Circuitos II.

"""


from splane import bodePlot, pzmap
from matplotlib import pyplot as plt
import scipy.signal as sig
from scipy.signal import TransferFunction as tf
import numpy as np

plt.close ( 'all' )

ripple_ = 3   # Ripple en la Banda de Paso, alfa_máx en dB


fp = 1000
#wp = 2*np.pi*fp

wp = 1  # Omega_p Normalizado.

order_filter = 2;

z, p, k = sig.buttap(order_filter)  # No Le Interesa el valor de epsilon.

NUM, DEN = sig.zpk2tf (z, p, k)

my_tf = tf (NUM, DEN)

#Ploteo:
bodePlot (my_tf)

pzmap (my_tf)   # Plano $ - Diagrama de Polos y Ceros
