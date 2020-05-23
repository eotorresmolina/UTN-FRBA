# -*- coding: utf-8 -*-
"""
Created on Mon May 11 00:37:56 2020

@author: Torres Molina Emmanuel O.
"""

"""
Comparación de dos Filtros Normalizados Pasa-Bajos Butterworth, Chebyshev y
Bessel de Orden 5, cuando filtran un "Tren de Pulsos" de pulsación angular
< 1/5 [rad/seg]

Voy a Suponer un w = 1/8 [rad/seg]

"""

# Importo los Paquetes, Métodos a Utilizar:
from splane import convert2SOS, analyze_sys, pretty_print_lti
from scipy.signal import TransferFunction as tfunction
from scipy.fftpack import fft
import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt

plt.close ( 'all' )


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

# Datos y Valores Dados:
w_pulso = 1/8    #  Pulsación Angular     [rad/seg]

#f_pulso = f_máx
f_pulso = w_pulso / (2*np.pi)  # Frecuencia Máxima
T_pulso = 1 / f_pulso   # Período del Pulso [seg]

wp = w_pulso
fp = f_pulso

wp_prima = wp / wp


# ----------------------------------------------------------------------------

# Proceso de Muestreo:
    
fN = 200 * f_pulso   # Frecuencia de Nyquist: fN >= 2*Fmáx

Ts = 1 / fN  # Período de Sampling
Fs = 1/Ts  # Frecuencia de Sampling

# Para Mostrar 3 Períodos del Pulso
N = 601 # Cantidad de Muestras.

t0 = 0
dt = Ts
tf = (N-1)*Ts

# Grilla de Sampleo Temporal
t = np.linspace (t0, tf, N) # array temporal de 601 muestras equispaciadas Ts.

# Onda Cuadrada
wave_square = sig.square (2 * np.pi * f_pulso * t )

# Conformo el Tren de Pulsos de Amplitud 1V:
train_pulse = (wave_square >= 0)
train_pulse = train_pulse * 1

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

# Diseño los Filtros Normalizados de Orden 5 para Luego Compararlos:

orden_filtro = 5       # Orden de los Filtros.
eps = 0.311 

# ----------------------------------------------------------------------------

print ('\n\nFiltro Butterworth de Orden 5:\n')

# Filtro de Butterworth: Uso de los Métodos dentro del Paquete signal de Scipy.
z1, p1, k1 = sig.buttap (orden_filtro)

# Obtengo los Coeficientes de mi Transferencia.
NUM1, DEN1 = sig.zpk2tf (z1, p1, k1)

# Cálculo de wb:
wb = eps ** (-1/orden_filtro)

# Obtengo la Transferencia Normalizada
my_tf_bw = tfunction ( NUM1, DEN1 )
print ('\n', my_tf_bw)

#pretty_print_lti(my_tf_bw)

print ('\nDenominador Factorizado de la Transferencia Normalizada:', convert2SOS ( my_tf_bw ))

NUM1, DEN1 = sig.lp2lp ( NUM1, DEN1, wb )
my_tf_bw = tfunction ( NUM1, DEN1 )

# ----------------------------------------------------------------------------

print ('\n\nFiltro Chebyshev de Orden 5:\n')

# Filtro de Chebyshev: Uso de los Métodos dentro del Paquete signal de Scipy.
z2, p2, k2 = sig.cheb1ap (orden_filtro, eps)

# Obtengo los Coeficientes de mi Transferencia.
NUM2, DEN2 = sig.zpk2tf (z2, p2, k2)

# Obtengo la Transferencia Normalizada
my_tf_ch = tfunction ( NUM2, DEN2 )
print ('\n', my_tf_ch)

#pretty_print_lti(my_tf_ch)

print ('\nDenominador Factorizado de la Transferencia Normalizada:', convert2SOS ( my_tf_ch ))


# ----------------------------------------------------------------------------

print ('\n\nFiltro Bessel de Orden 5:\n')

# Filtro de Bessel: Uso de los Métodos dentro del Paquete signal de Scipy.
z3, p3, k3 = sig.besselap ( orden_filtro, 'mag' )

# Obtengo los Coeficientes de mi Transferencia.
NUM3, DEN3 = sig.zpk2tf (z3, p3, k3)

# Obtengo la Transferencia Normalizada
my_tf_be = tfunction ( NUM3, DEN3 )
print ('\n', my_tf_be)

#pretty_print_lti(my_tf_be)

print ('\nDenominador Factorizado de la Transferencia Normalizada:', convert2SOS ( my_tf_be ))


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------


# Ploteo de las Señales, Respuestas, y Filtros:
my_tfs = [my_tf_bw , my_tf_ch, my_tf_be]

# Respuesta de Módulo y Fase
# Diagrama de Polos Y Ceros 
analyze_sys ( my_tfs, ['Butter Orden 5', 'Cheby Orden 5', 'Bessel Orden 5'] )

""" 
for i in range ( len(my_tfs) ):
    
    bodePlot ( my_tfs[i], 1)
    plt.legend (['Butter Orden 5', 'Cheby Orden 5', 'Bessel Orden 5'])
    pzmap ( my_tfs[i], 2 )
 """   

tt, y1, x = sig.lsim2 ((NUM1, DEN1), train_pulse, t )
tt, y2, x = sig.lsim2 ((NUM2, DEN2), train_pulse, t )
tt, y3, x = sig.lsim2 ((NUM3, DEN3), train_pulse, t )

fig7 = plt.figure ()
fig7.suptitle ("Tren de Pulsos de Amplitud 1V y de 0.125 [rad/seg] Muestreado a Ts = 0.251 seg durante 150 seg")
plt.plot (t, train_pulse, 'k')
plt.grid()
plt.xlabel ('t[seg]')
plt.ylabel ('x[t] [V]')
plt.xlim (0, (N-1)*Ts)
plt.ylim (-0.1, 1.1)


fig8 = plt.figure ( )
fig8.suptitle ( 'Comparación entre las Salidas al Aplicar el Filtro Pasa-Bajos' )
plt.plot (t, train_pulse, 'k')
plt.plot (t, y1, 'b')
plt.plot(t, y2, '#ff7f0e')
plt.plot (t, y3, 'g')
plt.legend ( ['Tren de Pulsos', 'Salida Filtro LP Butter Orden 5', 'Salida Filtro LP Cheby Orden 5', 'Salida Filtro LP Bessel Orden 5'] )
plt.grid()
plt.xlabel ('time [seg]')
plt.ylabel ('y(t) [V]')
plt.xlim (0, (N-1)*Ts)
plt.ylim (-0.15, 1.2)


# ----------------------------------------------------------------------------

# Ploteo Espectral:

# Grilla de Sampleo Frecuencial
f0 = 0
df = Fs/N 
f_f = (N-1)*df
ff = np.linspace (f0, f_f, N)


X = np.abs ( fft (train_pulse)  ) 
Y1 = np.abs ( fft (y1)  )
Y2 = np.abs ( fft (y2)  )
Y3 = np.abs ( fft (y3)  )

fig9 = plt.figure ( )
fig9.suptitle ( 'Comparación de la FFT del Tren de Pulsos' )
plt.plot (ff[1:], X[1:], 'k')
plt.plot (ff[1:], Y1[1:], 'b' )
plt.plot (ff[1:], Y2[1:], '#ff7f0e' )
plt.plot (ff[1:], Y3[1:], 'g' )
plt.legend ( ['FFT del Tren de Pulsos', 'FFT del Filtro Butter', 'FFT del Filtro de Cheby', 'FFT del Filtro de Bessel'] )
plt.grid ( )
plt.xlabel ( 'Frecuency [Hz]' )
plt.ylabel ( 'Magnitude Response' )
plt.xlim (0.001, f_f/2)