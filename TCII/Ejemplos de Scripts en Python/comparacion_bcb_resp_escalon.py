# -*- coding: utf-8 -*-
"""
Created on Thu May 21 23:10:20 2020

@author: Emmanuel Torres Molina
"""

"""
Comparación de dos Filtros Normalizados Pasa-Bajos Butterworth, Chebyshev y
Bessel de Orden 5, cuando filtran una Señal de Entrada Escalón.
Comparación de la Respuesta Indicial o Respuesta al Escalón.
Comparación de la Respuesta al Impulso h(t)

"""

from splane import bodePlot, pzmap, convert2SOS, analyze_sys, pretty_print_lti
from t_resp_step import peak_time_mag, settling_time_step_resp, rise_time
from t_resp_step import esc as u
from scipy.signal import TransferFunction as tfunction
import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt

plt.close ( 'all' )


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------


# Proceso de Muestreo:
    
f_pulso = (1/8) / (2*np.pi)  
    
fN = 200 * f_pulso   # Frecuencia de Nyquist: fN >= 2*Fmáx

Ts = 1 / fN  # Período de Sampling
Fs = 1/Ts  # Frecuencia de Sampling

N = 601 # Cantidad de Muestras.

t0 = 0
dt = Ts
tf = (N-1)*Ts

# Grilla de Sampleo Temporal
t = np.linspace (t0, tf, N) # array temporal de 601 muestras equispaciadas Ts.

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

print ('Denominador Factorizado de la Transferencia Normalizada:', convert2SOS ( my_tf_be ))


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------


# Ploteo de las Señales, Respuestas, y Filtros:
my_tfs = [my_tf_bw , my_tf_ch, my_tf_be]

# Respuesta de Módulo y Fase
# Diagrama de Polos Y Ceros 
analyze_sys ( my_tfs, ['Butter Orden 5', 'Cheby Orden 5', 'Bessel Orden 5'] )


# ----------------------------------------------------------------------------

# Ploteo de la Señal "Escalón":
    
t0 = -(N // 8)*Ts
tf = np.ceil(N/2)*Ts
tt = np.linspace (t0, tf, N)

fig10 = plt.figure ( )
fig10.suptitle ('Unit Step Function')
plt.plot(tt, u(tt), 'k')
plt.xlabel ('time [seg]')
plt.ylabel ('Step Fuction $u(t)$ [V]')
plt.xlim (t0, tf/2)
plt.grid ( )


#  Calculo la Respuesta cuando la Entrada es un Escalón:
t_t, resp1_u, x = sig.lsim2 ((NUM1, DEN1), u(tt), tt)
t_t, resp2_u, x = sig.lsim2 ((NUM2, DEN2), u(tt), tt)
t_t, resp3_u, x = sig.lsim2 ((NUM3, DEN3), u(tt), tt)


print ('\n\n----------------------------------------------------------------')
print ('\nParámetros de la Respuesta al Escalón:')


tr1, mod1, porc_tr1 = rise_time (t_t, resp1_u)
tr2, mod2, porc_tr2 = rise_time (t_t, resp2_u)
tr3, mod3, porc_tr3 = rise_time (t_t, resp3_u)

print ('\n\nTiempo de Subida, en Alcanzar el 1er Cruce "tr", Amplitud y Porcentaje: \n')
print ('Butter:  ', [tr1, mod1, porc_tr1] )
print ('\nCheby:  ', [tr2, mod2, porc_tr2] )
print ('\nBessel:  ', [tr3, mod3, porc_tr3] )
print ('\n')


tp1, mp1, so1 = peak_time_mag (t_t, resp1_u)
tp2, mp2, so2 = peak_time_mag (t_t, resp2_u)
tp3, mp3, so3 = peak_time_mag (t_t, resp3_u)

print ('Tiempo en alcanzar el Pico Máximo "tp", Amplitud y Porcentaje: \n')
print ('Butter:  ', [tp1, mp1, so1] )
print ('\nCheby:  ', [tp2, mp2, so2] )
print ('\nBessel:  ', [tp3, mp3, so3] )
print ('\n')


ts1, porc_ts1, val_ts1 = settling_time_step_resp (t_t, resp1_u)
ts2, porc_ts2, val_ts2 = settling_time_step_resp (t_t, resp2_u)
ts3, porc_ts3, val_ts3 = settling_time_step_resp (t_t, resp3_u)

print ('Tiempo de Establecimiento "ts" y su Porcentaje: \n')
print ('Butter:  ', [ts1, porc_ts1] )
print ('\nCheby:  ', [ts2, porc_ts2] )
print ('\nBessel:  ', [ts3, porc_ts3] )
print ('\n\n')


fig11 = plt.figure ( )
plt.suptitle ( 'Comparación Filtro LP Orden 5, Respuesta cuando la entrada es un Escalón' )
plt.plot (t_t, u(t_t), 'k')

plt.plot (t_t, resp1_u, 'b')
plt.text (tp1, mp1, '$MP1$', fontsize = 12 )
plt.text (ts1, 0.0, '$ts_1$', fontsize = 15 )

plt.plot (t_t, resp2_u, '#ff7f0e')
plt.text (tp2, mp2, '$MP2$', fontsize = 12 )
plt.text (ts2, 0.0, '$ts_2$', fontsize = 15 )

plt.plot (t_t, resp3_u, 'g')
plt.text (tp3, mp3, '$MP3$', fontsize = 12 )
plt.text (ts3, 0.0, '$ts_3$', fontsize = 15 )

plt.plot (tp1, mp1, 'mo')
plt.plot (tp2, mp2, 'mo')
plt.plot (tp3, mp3, 'mo')

plt.plot ([ts1, ts1], [0.0, val_ts1], 'ko')
plt.plot ([ts2, ts2], [0.0, val_ts2], 'ko')
plt.plot ([ts3, ts3], [0.0, val_ts3], 'ko')


plt.legend ( ['Escalón Unitario', '$Butter$', '$Cheby$', '$Bessel$'] )
plt.xlabel ('time [seg]', fontsize = 12)
plt.ylabel ('Step Response $c(t)$ [V]', fontsize = 12)
plt.grid ( )
plt.xlim (t0, tf*9/10)


# ----------------------------------------------------------------------------

# Respuesta al Impulso: h(t):

t, resp1_h = sig.impulse2 ( my_tf_bw, None, t )
t, resp2_h = sig.impulse2 ( my_tf_ch, None, t )
t, resp3_h = sig.impulse2 ( my_tf_be, None, t )

fig12 = plt.figure ( )
plt.suptitle ( 'Comparación: Respuesta al Impulso h(t)' )
plt.plot (t, resp1_h, 'b')
plt.plot (t, resp2_h, '#ff7f0e')
plt.plot (t, resp3_h, 'g')
plt.legend ( ['$Butter$', '$Cheby$', '$Bessel$' ] )
plt.xlabel ('time [seg]', fontsize = 12)
plt.ylabel ('Impulse Response $h(t)$', fontsize = 12)
plt.grid ( )
plt.xlim (-1, 45)