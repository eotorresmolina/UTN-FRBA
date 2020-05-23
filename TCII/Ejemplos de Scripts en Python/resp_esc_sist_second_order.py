# -*- coding: utf-8 -*-
"""
Created on Fri May 22 17:12:43 2020

@author: Emmanuel Torres Molina
"""

"""

Comparación de la Respuesta al Escalón para Sistemas Low-Pass de 2do Orden:
# Según como varía el factor de Amortigüamiento del Sistema.
# Según como varía el Q: Factor de Selectividad del Sistema.

"""


from t_resp_step import step_resp_SecondOrder, step_resp_SecondOrder2
from t_resp_step import esc as u
import matplotlib.pyplot as plt
import numpy as np

plt.close ( 'all' )


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------


# Grilla de Sampleo Temporal:

Amp = 5 # Amplitud del Escalón
w0 = 100 # Pulsación Angular [rad/seg]    

N = 802     # Cantidad de Muestras
fN = 1000

# Sampleo
Fs = fN
Ts = 1 / Fs    # Período de Sampling

t0 = -(N//8)*Ts
dt = Ts
tf = (N//2)*Ts
t = np.linspace (t0, tf, N)

# ----------------------------------------------------------------------------

# Defino los Factores de Amortigümiento del Sistema:
f_amort1 = 0.25
f_amort2 = 1.
f_amort3 = 4.

my_factor_amort = [f_amort1, f_amort2, f_amort3]

resp_f_amort = np.zeros ( (len(my_factor_amort), len (t) ) )

for n in range ( len(my_factor_amort) ):
    
    tt, resp_f_amort[n] = step_resp_SecondOrder (t, my_factor_amort[n], w0, Amp)


# ----------------------------------------------------------------------------    

# Defino los Q: Factor de Selectividad del Sistema:
qq1 = 2
qq2 = 0.5
qq3 = 0.25

my_qq = [qq1, qq2, qq3]

resp_Q = np.zeros ( ( len(my_qq), len(t) ) )

for n in range ( len(my_qq) ):
    
    tt, resp_Q[n] = step_resp_SecondOrder2 (t, my_qq[n], w0, Amp)
    
    
# ----------------------------------------------------------------------------

# Gráfica de la Entrada y las Respuestas:

# Comparación del Factor de Amortigüamiento del Sistema:
fig1 = plt.figure ( )
plt.title ('Respuesta al Escalón de un Sistema de 2do Orden y Comparación del "Factor de Amortigüamiento" ($\\xi$)')
plt.grid ( )
plt.xlim (t0, tf)
plt.xlabel ('$time [seg]$', fontsize = 12)
plt.ylabel ('$c(t)$', fontsize = 18)
plt.plot(tt, resp_f_amort[0], 'r')
plt.plot(tt, resp_f_amort[1], 'g')
plt.plot(tt, resp_f_amort[2], 'b')
plt.legend ( ['Sistema Subamortiguado: $\\xi = 0.25 < 1$', 'Sistema con Amortigüamiento Crítico: $\\xi = 1$', 'Sistema Sobreamortigüado: $\\xi = 4 > 1$'] )
plt.plot(t, Amp*u(t), 'k')


# Comparación del Q: Factor de Selectividad del Sistema:
fig2 = plt.figure ( )
plt.title ('Respuesta al Escalón de un Sistema de 2do Orden y Comparación del "Factor de Selectividad" ($Q$)')
plt.grid ( )
plt.xlim (t0, tf)
plt.xlabel ('$time [seg]$', fontsize = 12)
plt.ylabel ('$c(t)$', fontsize = 18)
plt.plot(tt, resp_Q[0], 'r')
plt.plot(tt, resp_Q[1], 'g')
plt.plot(tt, resp_Q[2], 'b')
plt.legend ( ['Sistema Subamortiguado: $Q = 2$', 'Sistema con Amortigüamiento Crítico: $Q = 0.5$', 'Sistema Sobreamortigüado: $Q = 0.25$'] )
plt.plot(t, Amp*u(t), 'k')