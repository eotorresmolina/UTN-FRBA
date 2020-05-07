# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 18:25:33 2020

@author: Emmanuel Torres Molina
"""

"""
Ejercicio que sirve para Comparar un Filtro de Butterworth (eps = 1)
o un Filtro de Máxima Planicidad (eps != 1) High - Pass Normalizados!!
Sólo se debe modificar el valor de: fp, fs, alfa_máx, alfa_mín
Si se quiere Ganancia modificar el valor de my_k (en veces)
"""

from splane import bodePlot, pzmap
from scipy.signal import TransferFunction as tf
import scipy.signal as sig
from matplotlib import pyplot as plt
import numpy as np

plt.close ('all')

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Requisitos de la Plantilla Destino High-Pass:

ripple_ = 1   ## alfa_máx en dB
attenuation_ = 35   ## alfa_mín en dB

fp_hp = 3500 # frecuencia de corte.
wp_hp = 2*np.pi*fp_hp
fs_hp = 1000
ws_hp = 2*np.pi*fs_hp

# Pulsaciones Angulares Normalizadas / Norma_frec = wp
wp_hp_prima = wp_hp/wp_hp  
ws_hp_prima = ws_hp/wp_hp

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Voy a Utilizar un Filtro Prototipo Low Pass y luego hacer una Transformación
# en Frecuencia.

# Requisitos de la Plantilla Fuente o Filtro Prototipo Low-Pass:

# Transformación en Frecuencia: wp_lp = -1/wp_hp
wp_lp = abs (-1/wp_hp)
ws_lp = abs (-1/ws_hp)
wp_lp_prima = abs (-1/wp_hp_prima)
ws_lp_prima = abs (-1/ws_hp_prima)

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Cálculo de epsilon y Orden del Filtro:

if ( ripple_ == 3 ):    # Si alfa_máx es 3dB estoy en el Caso de Butterworth
    eps = 1             # epsilon = 1
    wb = 1  #Omega de Butterworth
    
else:
    eps = np.sqrt ( 10**(ripple_/10) - 1 )
  
    
orden_filtro = np.log(((10**(attenuation_/10) - 1)/(eps**2)))/(2 * np.log(ws_lp_prima))

N = orden_filtro

if ( orden_filtro >= ( int ( orden_filtro ) + 0.05 ) ):
    orden_filtro = int (orden_filtro) + 1
    
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Hallo el Numerador y Denominador de mi Transferencia Prototipo Low-Pass

# Calculo los Ceros, Polos y K(Ganancia) de mi filtro, según el Orden.
z, p, k = sig.buttap (orden_filtro) # Aprox. Butterworth ==> No le importa el eps.

# Calculo del Numerador y Denominador
NUM, DEN = sig.zpk2tf ( z, p, k )

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Genero el Filtro Prototipo Low Pass

if (eps != 1 ):  # Caso de Máxima Planicidad!!

    wb_lp = eps**( -1/orden_filtro )    # Omega de Butterworth Low Pass
    NUM_lp, DEN_lp = sig.lp2lp ( NUM, DEN, wb_lp )   # Renormalizo con wb_lp
    
else:
    NUM_lp, DEN_lp = sig.lp2lp ( NUM, DEN )   # Caso de Butterworth

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Llevo mi Filtro Prototipo (Low-Pass) a mi Filtro Destino (High-Pass)

if (eps != 1 ):  # Caso de Máxima Planicidad!!

    wb_hp = 1 / abs (wb_lp)    # Omega de Butterworth High Pass
    NUM_hp, DEN_hp = sig.lp2hp ( NUM, DEN, wb_hp )   # Renormalizo con wb_hp
    
else:
    NUM_hp, DEN_hp = sig.lp2hp ( NUM, DEN )   # Caso de Butterworth
    
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Calculo la Transferencia de mi Filtro Objetivo (High-Pass)

my_tf_lp = tf (NUM_lp, DEN_lp)    
my_tf_hp = tf (NUM_hp, DEN_hp)

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Ploteo

bodePlot ( my_tf_hp, 'Filtro High Pass' )
pzmap ( my_tf_hp, 'none', 'Filtro Destino - High Pass' ) 
pzmap ( my_tf_lp, 'none', 'Filtro Prototipo - Low Pass' )


