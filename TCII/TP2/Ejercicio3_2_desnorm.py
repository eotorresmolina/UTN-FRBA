# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 14:36:18 2020

@author: Emmanuel Torres Molina
"""
"""
Ejercicio 3_2 Desnormalizado del TP2 de Teoría de los Circuitos II.
Sólo Modificar el Valor de alfa_máx, alfa_mín, fp, fs, y los elementos
del circuito (R1, R3, R4, C2, C5), cuya estructura es un MFB (Multiple 
FeedBack) Low-Pass.
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
attenuation_ = 20   ## alfa_mín en dB

fp = 10**3 # frecuencia de corte.
wp = 2*np.pi*fp
fs = 2000
ws = 2*np.pi*fs

# Pulsaciones Angulares Normalizadas / Norma_frec = wp
wp_prima= wp/wp  
ws_prima = ws/wp

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Parámetros de Diseño del MFB (Multiple FeedBack):

# Etapa 1:
    
# Elementos
R1_1 = 2000
R3_1 = 1618
R4_1 = R1_1
C2_1 = 129e-9
C5_1 = 40e-9

k1 = -R4_1/R1_1
qq1 = 1/( np.sqrt((R4_1*C5_1)/(R3_1*C2_1))+ np.sqrt((R3_1*C5_1)/(R4_1*C2_1)) + (1/R1_1)*(np.sqrt(R3_1*R4_1*C5_1/C2_1)) )

# Etapa 2:
    
# Elementos
R1_2 = 10**4
R3_2 = 2392
R4_2 = R1_2
C2_2 = 129e-9
C5_2 = 5e-9

k2 = -R4_2/R1_2
qq2 = 1/( np.sqrt((R4_2*C5_2)/(R3_2*C2_2))+ np.sqrt((R3_2*C5_2)/(R4_2*C2_2)) + (1/R1_2)*(np.sqrt(R3_2*R4_2*C5_2/C2_2)) )


# Etapa 3: Etapa Integradora
    
# Elementos
R1_3 = 10**4
C1_3 = 13e-9

k3 = 1

# Etapa de Ganancia:
R4n = 1000
R5n = 9000
    
k4 = 1 + (R5n/R4n)


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
den3 = [ 0, 1, 1 ] 

p1 = np.roots ( den1 )
p2 = np.roots ( den2 )
p3 = np.roots ( den3 )

# Genero los Zeros, Polos y K (Ganancia)
my_z = np.array ( [ ] )
my_p = np.concatenate ( (p1, p2, p3), axis = None )
my_k = k1*k2*k3*k4     # Ganancia Total del Circuito (en veces)

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Genero el Numerador y Denominador de mi Filtro:
NUM, DEN = sig.zpk2tf ( my_z, my_p, my_k )

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Se ejecuta Únicamente si estoy en el Caso de MÁXIMA PLANICIDAD !!! eps != 1
if ( eps != 1 ):   
    wb = eps**(-1/order_filter) #Omega de Butterworth
   # NUM, DEN = sig.lp2lp ( NUM, DEN, wb )   # Renormalizo para wb
  
# Vuelvo a Calcular el valor de norma_frec con los valores desnormalizados.
norma_frec = 1  / np.sqrt ( R3_1*R4_1*C2_1*C5_1 )


# Desnormalizo a Nivel de Frecuencia / norma_frec = wp
NUM, DEN = sig.lp2lp ( NUM, DEN, norma_frec )

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Calculo de la Transferencia
my_tf = tf ( NUM, DEN )

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Ploteo
bodePlot ( my_tf )
pzmap ( my_tf )