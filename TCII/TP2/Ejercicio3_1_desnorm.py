# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 23:46:25 2020

@author: Emmanuel Torres Molina
"""

"""
Ejercicio 3_1 Desnormalizado del TP2 de Teoría de los Circuitos II.
Sólo Modificar el Valor de alfa_máx, alfa_mín, fp, fs, y los elementos
del circuito (R, Rb, C), cuya estructura es un Sallen-Key Low-Pass.
"""

from splane import bodePlot, pzmap
import scipy.signal as sig
from scipy.signal import TransferFunction as tf
from matplotlib import pyplot as plt
import numpy as np

plt.close ('all')

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

ripple_ = 0.5    ## alfa_máx en dB
attenuation_ = 30   ## alfa_mín en dB

fp = 10**3 # frecuencia de corte.
wp = 2*np.pi*fp
fs = 2330
ws = 2*np.pi*fs

# Pulsaciones Angulares Normalizadas / Norma_frec = wp
wp_prima= wp/wp  
ws_prima = ws/wp

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Parámetros de Diseño del Sallen- Key:

# Etapa 1:
    
# Elementos
R1 = 10**4
RB1 = 680
C1 = 13e-9

k1 = 1+(RB1/R1)
qq1 = 1/(3-k1)

# Etapa 2:
    
# Elementos
R2 = 10**4
RB2 = 5860
C2 = 13e-9

k2 = 1+(RB2/R2)
qq2 = 1/(3-k2)

# Etapa 3:
    
# Elementos
R3 = 10**4
RB3 = 14820
C3 = 13e-9

k3 = 1+(RB3/R3)
qq3 = 1/(3-k3)

# Etapa de Ganancia:
R4 = 1000
R5 = 1400
    
k4 = 1 + (R5/R4)


eps = np.sqrt ( 10**(ripple_ /10) - 1 )     # epsilon = ripple en Band Pass

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Calculo el Orden del Filtro 
order_filter = np.log( (10**(attenuation_ /10) - 1 ) / (eps**2) ) / ( 2 * np.log(ws_prima) )

N = order_filter

# En caso de que N sea decimal redondeo al nro entero mas grande
if ( order_filter >= (int (order_filter) + 0.05) ):
    
    order_filter = int (order_filter) + 1
    
    
# Genero los Denominadores de las Transferencias de cada Etapa.

den1 = [ 1, 1/qq1, 1 ] 

den2 = [ 1, 1/qq2, 1 ] 

den3 = [ 1, 1/qq3, 1 ] 

p1 = np.roots ( den1 )
p2 = np.roots ( den2 )
p3 = np.roots ( den3 )

# Genero los Zeros, Polos y K (Ganancia)
my_z = np.array ( [ ] )
my_p = np.concatenate ( (p1, p2, p3), axis = None )
my_k = k1*k2*k3*k4      # Ganancia Total del Circuito (en veces)

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Genero el Numerador y Denominador de mi Filtro:
NUM, DEN = sig.zpk2tf ( my_z, my_p, my_k )

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Se ejecuta Únicamente si estoy en el Caso de MÁXIMA PLANICIDAD !!! eps != 1
if ( eps != 1 ):   
    wb = eps**(-1/order_filter) #Omega de Butterworth    
    
    
norma_frec = 1 / (R1*C1)    # Calculo la Norma de Desnormalización     
NUM, DEN = sig.lp2lp ( NUM, DEN, norma_frec ) # Desnormalizo usando la norma de Frecuencia.

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Calculo de la Transferencia
my_tf = tf ( NUM, DEN )

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Ploteo
bodePlot ( my_tf )
pzmap ( my_tf )
