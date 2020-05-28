# -*- coding: utf-8 -*-
"""
Created on Wed May 27 23:35:02 2020

@author: Emmanuel Torres Molina
"""

"""

Script que permite Comparar y Graficar la Respuesta en Módulo y Fase como el
Retardo de Grupo de laTransferencia de un Filtro Chebychev Tipo I y un 
Filtro Chebyshev Tipo II o Chebyshev Inverso para un Orden Dado.

"""

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

from splane import analyze_sys
from scipy.signal import TransferFunction as tf
import scipy.signal as sig
from matplotlib import pyplot as plt

plt.close ('all')

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Defino los Parámetros a Utilizar:
    
alfa_max = 3   # dB    Máxima Atenuación en la Banda de Paso.
alfa_min = 40   #dB    Mínima Atenuación en la Banda de Stop.

eps = 1   # Ripple

my_N = [2, 3, 4]  #Orden de mis Filtros.

# Diseño de los Filtros:

    
# ---------------------------------------------------------------------------
    
# N = 2:
    
# Filtro Chebyshev Tipo I:
z1, p1, k1 = sig.cheb1ap ( my_N[0], eps )
NUM1, DEN1 = sig.zpk2tf (z1, p1, k1)
tf_ch1 = tf ( NUM1, DEN1 )

# Filtro Chebyshev Tipo II o Chebyshev Inverso:
z2, p2, k2 = sig.cheb2ap ( my_N[0], alfa_min )
NUM2, DEN2 = sig.zpk2tf (z2, p2, k2)
tf_ch2 = tf ( NUM2, DEN2 )


analyze_sys ([tf_ch1, tf_ch2], ['Cheby Tipo I Orden 2', 'Cheby Tipo II o Inverso Orden 2'])


# ---------------------------------------------------------------------------

# N = 3:
    
# Filtro Chebyshev Tipo I:
z1, p1, k1 = sig.cheb1ap ( my_N[1], eps )
NUM1, DEN1 = sig.zpk2tf (z1, p1, k1)
tf_ch1 = tf ( NUM1, DEN1 )

# Filtro Chebyshev Tipo II o Chebyshev Inverso:
z2, p2, k2 = sig.cheb2ap ( my_N[1], alfa_min )
NUM2, DEN2 = sig.zpk2tf (z2, p2, k2)
tf_ch2 = tf ( NUM2, DEN2 )

analyze_sys ([tf_ch1, tf_ch2], ['Cheby Tipo I Orden 3', 'Cheby Tipo II o Inverso Orden 3'])


# ---------------------------------------------------------------------------

# N = 4:
    
# Filtro Chebyshev Tipo I:
z1, p1, k1 = sig.cheb1ap ( my_N[2], eps )
NUM1, DEN1 = sig.zpk2tf (z1, p1, k1)
tf_ch1 = tf ( NUM1, DEN1 )

# Filtro Chebyshev Tipo II o Chebyshev Inverso:
z2, p2, k2 = sig.cheb2ap ( my_N[2], alfa_min )
NUM2, DEN2 = sig.zpk2tf (z2, p2, k2)
tf_ch2 = tf ( NUM2, DEN2 )

analyze_sys ([tf_ch1, tf_ch2], ['Cheby Tipo I Orden 4', 'Cheby Tipo II o Inverso Orden 4'])