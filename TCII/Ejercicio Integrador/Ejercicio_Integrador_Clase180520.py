# -*- coding: utf-8 -*-
"""
Created on Mon May 25 22:35:06 2020

@author: Emmanuel Torres Molina
"""

"""
Ejercicio Integrador planteado en Clase.

Se debe diseñar un filtro pasaaltos , que presente máxima planicidad en la 
banda de paso (frecuencia de corte = 300Hz)  y un cero  de transmisión en 
100 Hz.
El prototipo pasabajos normalizado presenta los siguientes Datos:
alfa_máx = 3dB para w0 normalizado = 1 rad/seg
N (Orden del Filtro): 3

Link:
https://docs.google.com/document/d/1k2fiWagX26f-GrcmwZtRlWYSxn0LL0eJAPZm91TWAuU/edit

"""

# ----------------------------------------------------------------------------

from splane import bodePlot, pzmap
from scipy.signal import TransferFunction as transf_f
from scipy.fftpack import fft
from scipy import signal as sig
import numpy as np
from matplotlib import pyplot as plt

plt.close ('all')


# ----------------------------------------------------------------------------

# Datos:

fp_hp = 300    # [Hz] Frecuencia de Corte
wp_hp = 2 * np.pi * fp_hp

f_zt_hp = 100   # Cero de Transmisión [Hz]
w_zt_hp = 2 * np.pi * f_zt_hp

alfa_max = 3 #dB
orden_filtro = 3

# Como alfa_máx = 3dB, supongo:
eps = 1     # Caso Butterworth Puro

# Normalizo a Nivel de Frecuencia, norma = wp_hp
wp_hp_n = wp_hp / wp_hp
w_zt_hp_n = w_zt_hp / wp_hp


# ----------------------------------------------------------------------------

# Filtro Prototipo Low-Pass:

# Transformación en Frecuencia: ====>    w_hp = -1 / w_lp
wp_lp_n = -1 / wp_hp_n
wp_lp_n = np.abs (wp_lp_n)

w_zt_lp_n = -1 / w_zt_hp_n
w_zt_lp_n = np.abs ( w_zt_lp_n )


z_lp_n, p_lp_n, k_lp_n = sig.buttap ( orden_filtro )
NUM_LP_n, DEN_LP_n = sig.zpk2tf ( z_lp_n, p_lp_n, k_lp_n )

NUM_LP_n = [1, 0, 9] # Le agrego el cero de transmisión.

my_tf_lp_n = transf_f (NUM_LP_n, DEN_LP_n)

bodePlot (my_tf_lp_n)
pzmap (my_tf_lp_n)


# ----------------------------------------------------------------------------

# Filtro Destino High-Pass:    
NUM_HP_n, DEN_HP_n = sig.lp2hp ( NUM_LP_n, DEN_LP_n )
z_hp_n, p_hp_n, k_hp_n = sig.tf2zpk ( NUM_HP_n, DEN_HP_n )

my_tf_hp_n = transf_f (NUM_HP_n, DEN_HP_n)

bodePlot (my_tf_hp_n)
pzmap (my_tf_hp_n)

# Si ahora quiero que para w--> inf haya 0dB:
k_hp_n = k_hp_n * (1/9)
NUM_HP_n, DEN_HP_n = sig.zpk2tf (z_hp_n, p_hp_n, k_hp_n)
my_tf_hp_n = transf_f (NUM_HP_n, DEN_HP_n)

bodePlot (my_tf_hp_n)

# Desnormalizo: w0 = wp_hp
w0 = wp_hp

NUM_HP, DEN_HP = sig.lp2hp ( NUM_LP_n, DEN_LP_n, w0 )
z_hp, p_hp, k_hp = sig.tf2zpk (NUM_HP, DEN_HP)
k_hp = k_hp * (1/9)

NUM_HP, DEN_HP = sig.zpk2tf (z_hp, p_hp, k_hp)

my_tf_hp = transf_f (NUM_HP, DEN_HP)

bodePlot (my_tf_hp)


# ----------------------------------------------------------------------------

"""

# Ejemplo de Filtrado de una Señal de 100 Hz

f_x = 100 # [Hz]
w_x = 2 * np.pi * f_x
T_x = 1 / f_x


fN = 2 * f_x             # Frecuencia de Nyquist
Fs = 20 * fN  # Frecuencia de Sampling
Ts = 1 / Fs  

N = 401

# Grilla de Sampleo Temporal:
t0 = 0
dt = Ts
tf = (N-1)*dt
t = np.linspace (t0, tf, N)

x = 1 * np.sin (w_x * t)

# Grilla de Sampleo Frecuencial:
f0 = 0
df = Fs/N
ff = (N-1)*df
f_f = np.linspace (f0, ff, N)

X = np.abs ( fft (x) )

fig9, axs = plt.subplots (2, 1)
plt.suptitle ('Señal a Filtrar y su FFT:')
axs[0].plot (t, x, 'b' )
axs[0].set_xlim (t0, tf)
axs[0].set_ylabel ('$x(t)$ [V]', fontsize = 13)

axs[1].plot(f_f, X, 'b')
axs[1].set_xlim (f0, Fs/2)
axs[1].set_xlabel ('$frecuency [Hz]$', fontsize = 12)
axs[1].set_ylabel ('$Ck$', fontsize = 14)


tt, y, xx = sig.lsim2 ((NUM_HP, DEN_HP), x, t)

Y = np.abs ( fft (y) )

fig10, axs = plt.subplots (2, 1)
plt.suptitle ('Señal Filtrada y su FFT:')
axs[0].plot (tt, y, 'k' )
axs[0].set_xlim (t0, tf)
axs[0].set_ylabel ('$y(t)$ [V]', fontsize = 13)

axs[1].plot(f_f, Y, 'k')
axs[1].set_xlim (f0, Fs/2)
axs[1].set_xlabel ('$frecuency [Hz]$', fontsize = 12)
axs[1].set_ylabel ('$Ck$', fontsize = 14)

"""