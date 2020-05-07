# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:51:36 2020

@author: Emmanuel Torres Molina
"""

"""
Ejercicio que sirve para Comparar un Filtro de Butterworth (eps = 1)
o un Filtro de Máxima Planicidad (eps != 1) Low - Pass Normalizado!!
Sólo se debe modificar el valor de: fp, fs, alfa_máx, alfa_mín
Si se quiere Ganancia modificar el valor de my_k (en veces)
"""

from splane import bodePlot, pzmap
import scipy.signal as sig
from scipy.signal import TransferFunction as tf
from matplotlib import pyplot as plt
import numpy as np

plt.close ('all')

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Requisitos de la Plantilla Low-Pass:

ripple_ = 3   ## alfa_máx en dB
attenuation_ = 18   ## alfa_mín en dB

fp = 500 # frecuencia de corte.
wp = 2*np.pi*fp
fs = 1500
ws = 2*np.pi*fs

# Pulsaciones Angulares Normalizadas / Norma_frec = wp
wp_prima= wp/wp  
ws_prima = ws/wp


if ( ripple_ == 3 ):
    eps = 1
    
else:
    eps = np.sqrt ( 10**(ripple_ /10) - 1 )   # epsilon = ripple en Band Pass

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Calculo el Orden del Filtro 
order_filter = np.log( (10**(attenuation_ /10) - 1 ) / (eps**2) ) / ( 2 * np.log(ws_prima) )

N = order_filter

# En caso de que N sea decimal redondeo al nro entero mas grande
if ( order_filter >= (int (order_filter) + 0.05) ):
    
    order_filter = int (order_filter) + 1

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Calculo de Ceros, Polos y Ganancia(k) dado el Orden del Filtro. Low-Pass

z, p, k = sig.buttap ( int(order_filter) ) #Filtro Butterworth / no le importa el eps

my_k = 10  # Agrego la Ganacia que Deseo: my_k (en veces)
k = my_k * k # Ganancia Total del Filtro

NUM, DEN = sig.zpk2tf ( z, p, k ) # Genero el Numerador y Denominador

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Se ejecuta Únicamente si estoy en el Caso de MÁXIMA PLANICIDAD !!! eps != 1
if ( eps != 1 ):   
    wb = eps**(-1/order_filter) #Omega de Butterworth
    
    NUM, DEN = sig.lp2lp ( NUM, DEN, wb )   # Renormalizo para wb

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Cálculo de la Transferencia
my_tf = tf ( NUM, DEN )

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Ploteo
bodePlot ( my_tf )
pzmap ( my_tf )







