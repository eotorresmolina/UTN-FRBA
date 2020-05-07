# -*- coding: utf-8 -*-
"""
Created on Sat May  2 21:31:37 2020

@author: Emmanuel Torres Molina
"""

"""
Ejercicio 10 del TP2 de Teoría de los Circuitos II:
Un tono de 45 KHz y 200 mV de amplitud es distorsionada por un tono de 12 KHz 
y 2V de amplitud. Diseñar un filtro pasa altos que atenúe la señal
interferente, de tal forma que el remanente no sea mayor que el 2% de los 200 mV.
La ganancia en alta frecuencia deberá ser de 0 db y la máxima atenuación
en la banda de paso menor a 1 dB. Emplear la aproximación que necesite menor 
número de etapas.
En este caso el Filtro está Sintetizado por un Estructura RLC Pasiva + RL Pasivo.
"""

import numpy as np
from scipy.signal import TransferFunction as transf_f
import scipy.signal as sig
from splane import bodePlot, pzmap
from matplotlib import pyplot as plt

plt.close ('all')

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Vector Tiempo:
t0 = 0.0    # Tiempo Inicial
tf = 0.005
dt = 0.00005  # Incremento
t = np.arange (t0, tf, dt)

# ---------------------------------------------------------------------------

# Tono de Interés:

f_t = 45 * 10**3 # Frecuecia del Tono de mi Interés [Hz]
w_t = 2 * np.pi * f_t # [rad/seg]
A_t = 0.2 # Amplitud de mi Tono [V]

s_t = A_t * np.sin ( w_t * t )

# ---------------------------------------------------------------------------

# Ruido Interferente:

f_r = 12 * 10**3         # Frecuencia del Ruido Interferente [Hz]
w_r = 2 * np.pi * f_r   # [rad/seg]
A_r= 2  # Amplitud del Ruido [V]

r_t = A_r * np.sin ( w_r * t )

sgnal = s_t + r_t

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Valores de los Elementos del Circuito:
    
# Etapa 1: RLC Pasivo
R1 = 290
C1 = 3.5e-9
L1 = 3.5e-3
k1 = 1

# Etapa 2: RL Pasivo
R2 = 700
C2 = 3.5e-9
L2 = 1.03e-3
k2 = 1


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Diseño del Filtro: Vamos a Realizar un Filtro High-Pass:
    
# Requisitos de Plantilla
alfa_max = 0.9 # Piden que sea menor a 1dB
alfa_min = 54 # el remanente no sea mayor que el 2% de los 200 mV
wp_hp = w_t
ws_hp = w_r

# Normalizo las Pulsaciones Angulares usando como norma: wp_hp
wp_hp_norm = wp_hp / wp_hp
ws_hp_norm = ws_hp / wp_hp

w0 = np.sqrt ( 1 / (L1*C1) )

# ---------------------------------------------------------------------------

# Filtro Prototipo Low-Pass: Transformación en Frecuencia: w_HP = -1 / w_LP
wp_lp_norm = abs(-1 / wp_hp_norm)
ws_lp_norm = abs(-1 / ws_hp_norm)


# Voy a Utilizar Aproximación de Chebyshev para Diseñal el Filtro:

eps = np.sqrt ( (10 **(alfa_max/10) ) - 1 )

# Orden del Filtro
N = np.arccosh ( np.sqrt ( (10**(alfa_min/10) - 1) / eps**2 ) ) / np.arccosh (ws_lp_norm)
N = np.ceil ( N )   # Redondeo para arriba

den1_lp = [1, 0.29, 1]
den2_lp = [1, 0.7, 0.29]

p1_lp = np.roots ( den1_lp )
p2_lp = np.roots ( den2_lp )

my_z_lp = np.array ([])
my_p_lp = np.concatenate ( (p1_lp, p2_lp), axis = None )
my_k_lp = 1 * 0.29

NUM, DEN = sig.zpk2tf ( my_z_lp, my_p_lp, my_k_lp )
NUM_lp, DEN_lp = sig.lp2lp ( NUM, DEN, w0 )

my_tf_lp = transf_f (NUM_lp,DEN_lp)

# ---------------------------------------------------------------------------

# Filtro Destino - Filtro High-Pass:
    
# Calculo W0:

NUM_hp, DEN_hp = sig.lp2hp ( NUM, DEN, w0 )

my_tf_hp = transf_f ( NUM_hp, DEN_hp )

my_z_hp, my_p_hp, my_k_hp = sig.tf2zpk (NUM_hp, DEN_hp )

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Filtrado de la Señal:
    
t, s_filtrada, x = sig.lsim2 ((my_tf_hp), sgnal, t )

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

# Ploteo de las Señales, Respuesta en Frecuencia, etc.

fig1, axs = plt.subplots(4,1)

axs[0].plot ( t, s_t )
axs[0].grid ('True')
axs[0].set_title ('Señal Original')
axs[0].set_ylim(-0.2,0.2)
axs[0].set_ylabel('[V]')

axs[1].plot ( t, r_t )
axs[1].grid ('True')
axs[1].set_title ('Ruido Interferente')
axs[1].set_ylabel('[V]')
axs[1].set_xlim(0)

axs[2].plot (t, s_t + r_t )
axs[2].grid ('True')
axs[2].set_title ('Señal a Filtrar')
axs[2].set_ylabel('[V]')
axs[2].set_xlim(0)

axs[3].plot (t, s_filtrada )
axs[3].grid ('True')
axs[3].set_title ( 'Señal Filtrada' )
axs[3].set_xlabel ('t[seg]')
axs[3].set_ylabel('[V]')
axs[3].set_ylim(-0.2,0.2)
axs[3].set_xlim(0)

# Respuesta en Frecuencia:
bodePlot (my_tf_lp, 'Filtro Prototipo - Low Pass')
pzmap (my_tf_lp)

bodePlot (my_tf_hp, 'Filtro Destino - High Pass')
pzmap (my_tf_hp)





 
