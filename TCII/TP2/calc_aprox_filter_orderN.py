# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 21:09:59 2020

@author: Emmanuel Torres Molina

"""

from splane import bodePlot, pzmap, grpDelay
import numpy as np
from scipy.signal import TransferFunction as tf
from scipy import signal as sig
from matplotlib import pyplot as plt

import sys

# Script que permite Calcular la Respuesta de Módulo y de Fase de una
# Transferencia dado el alfa_máx, alfa_mín y N según Requisitos de Plantilla.

plt.close('all')

print('\n\n\n')
print ("Tipos de Aproximación:")
print ("    Butterworth - Chebyshev1 - Bessel        ")

# Tipos de Aproximación:
print("\nIngrese Aproximación:  ")
aprox_name = input( )
#aprox_name = "Butterworth"
#aprox_name = "Chebyshev1"
#aprox_name = "Bessel"

print('\nIngrese Ripple (alfa_máx) en dB: ')
ripple_ = float ( input( ) )     ## Valor de alfa_máx en dB # Máxima Atenuación Band Pass

print('\nIngrese Atenuación Mínima (alfa_mín) en dB: ')
attenuation_ = float ( input( ) )     # Valor de alfa_mín en dB # Mínima Atenuación Band Stop


print ('\nIngrese Orden (Nro. Entero): ')
order_filter = int ( input ( ) )

if ( aprox_name == "Butterworth" ):
    
    # Paso el Orden y devuelve ceros, polos y Ganancia
    z, p, k = sig.buttap (order_filter)     # No le Interesa el ripple
    
    # Cálculo del Epsilon (Ripple)
    eps = np.sqrt ( 10**(ripple_/10) - 1 ) 
    
    wb = eps**(-1/order_filter)     # Omega_Butter / Renormalización.
    
    NUM, DEN = sig.zpk2tf (z, p, k)
    NUM, DEN = sig.lp2lp ( NUM, DEN, wb )
    
    z, p, k = sig.tf2zpk ( NUM, DEN ) 
    
    
elif (aprox_name == 'Chebyshev1'):
    
    # Le paso Orden y ripple (alfa_máx)
    z, p, k = sig.cheb1ap (order_filter, ripple_) 
    
    
elif (aprox_name == 'Bessel'):
    
    z, p, k = sig.besselap ( order_filter, norm = 'mag' )
    
    
else:
    
    sys.exit(' No Existe esa Aproximación o Está mal Escrita.')
    

# Genero el Numerador y Denominador de mi Transferencia
NUM, DEN = sig.zpk2tf(z, p, k)

my_tf = tf ( NUM, DEN ) # Genero mi Transferencia


# Ploteo.
bodePlot (my_tf)
pzmap (my_tf)
#grpDelay (my_tf)
    
  
        
        
    
    
    
    