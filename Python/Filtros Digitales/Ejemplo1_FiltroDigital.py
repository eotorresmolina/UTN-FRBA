# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 21:43:43 2020

@author: Emmanuel Torres Molina
"""

"""

1er Ejemplo de Filtros Digitales.

1) Sintetizar una Señal de 2 segundos con la suma de 3 cosenos de 100 Hz,
500 Hz y 1 KHz. Utilziar una Fs de 8000Khz

2) Mostrar el Espectro de la Señal (Espectro Módulo). Escalar el Eje de 
Frecuencia en Hz.

3) Diseñar un Filtro Pasa-Bajos de fc = 800 Hz. Obtener el h[n].
Utilizar un software como:
    fdatool
    pyfdax
    
4) Aplicar el Filtro Diseñado y mostrar la Salida Temporal junto con la Señal 
   de Entrada.
   
5) Calcular la Energía de la Señal en el Tiempo y la Energía de la Respuesta 
de Módulo.

"""


##############################################################################
##############################################################################

#%%
# Importo los Paquetes y Módulos que Voy a Utilizar:
from scipy.io import wavfile
from scipy.fft import fft
from scipy import signal as sig
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as im

plt.close ('all')  ## Cierro todas las Figuras que hayan quedado.


##############################################################################
##############################################################################


#%% 1) Sintetizar una Señal de 200 milisegundos con la suma de 3 cosenos de 100 
# Hz, 500 Hz y 1 KHz.

Fs = 8 * 10**3  # Frecuencia de Sampling
Ts = 1/Fs  # Período de Sampling
fN = Fs / 2 # Frecuencia de Nyquist

# Calculo la Cantidad de Muestras:
# Si Tomo una muestra cada Ts segundos, y la duración de la Señal quiero que 
# sea de 2 segundos ==> N = (2 * 1) / Ts
N = int (2 / Ts)

# Grilla Temporal
t0 = 0
dt = Ts
tf = (N-1)*dt
t = np.linspace(t0, tf, N)

s = 1 * np.cos(2*np.pi*100*t) + 1 * np.cos(2*np.pi*500*t) + 1 * np.cos (2*np.pi*1000*t)

# Disminuyo la Amplitud de la Señal Sintetizada para no Saturar, y para cuidar
# los parlantes.
s = s * (0.8 / np.max ( [np.abs(np.max(s)), np.abs(np.min(s))] ) )


#%% Ploteo de la Señal Sintetizada.

fig1 = plt.figure ( )
plt.plot (t, s, 'b')
plt.grid ('true')
plt.title('Señal Sintetizada')
plt.xlabel('$t[seg]$', fontsize = 15)
plt.ylabel('$s(t)$', fontsize = 15)


#%% Guardo la Señal Sintetizada como un audio de formato .wav

#s = np.uint8 (s)
wavfile.write ('ejemplo1_filtro_digital_in.wav', Fs, s)


##############################################################################
##############################################################################

#%% 2) Mostrar el Espectro de la Señal (Espectro Módulo). Escalar el Eje de 
# Frecuencia en Hz.

# Grilla Frecuencial
f0 = 0
df = Fs / N     # Resolución Espectral
ff = (N-1)*df
f = np.linspace(f0, ff, N)

# Calculo la TDF de la Señal Sintetizada Utilizando la FFT:
S = fft (s)
Abs_S = np.abs( S ) / N # Módulo


#%% Ploteo el Módulo del Espectro de la Señal Sintetizada.
fig2 = plt.figure ( )
plt.plot (f, Abs_S)
plt.title ('Módulo del Espectro de la Señal Sintetizada')
plt.grid ('true')
plt.xlabel('$frecuency [Hz]$', fontsize = 13)
plt.ylabel ('$|S(f)|$', fontsize = 15)


##############################################################################
##############################################################################

#%% 3) Diseñar un Filtro Pasa-Bajos de fc = 800 Hz. Obtener el h[n].
# Utilizar un software como:
#    fdatool
#    pyfdax

# En este caso Voy a Utilizar el "pyfdax" para diseñar el Filtro Digital.

# Obtengo los Coeficientes de mi h[n]
h = [ 
     -0.0019052994253283583,
     -0.0051037209977799905,
     -0.006457120692863402,
     -0.0053490336766239726,
     -0.0020929384168351124,
     0.0021448625834810824,
     0.00575723583485291,
     0.007299652155009577,
     0.006060704811784669,
     0.0023770620115118202,
     -0.002442166072386912,
     -0.006572654912253929,
     -0.008356875676633322,
     -0.006959029046721823,
     -0.002737940269069003,
     0.002822258606220101,
     0.007622325686837236,
     0.00972769699128124,
     0.00813273978512545,
     0.0032132640403633814,
     -0.0033271785203400823,
     -0.009029385997457956,
     -0.011582979285734997,
     -0.00973756094553485,
     -0.003870294351801647,
     0.004033290266404478,
     0.011021796776966134,
     0.014245496416753448,
     0.012074103313018496,
     0.004841923752344648,
     -0.005095292414297668,
     -0.01407399531145508,
     -0.018406948697547505,
     -0.01580739054584703,
     -0.006432533785285164,
     0.006881276659604978,
     0.01936333342722582,
     0.025865816447546524,
     0.022759061611784787,
     0.00952630233346234,
     -0.010534288909074228,
     -0.030837473835488727,
     -0.04321662753179002,
     -0.04035589196521442,
     -0.01822264184977342,
     0.02227763082733816,
     0.0750023262087275,
     0.1298104347390131,
     0.17504873741057997,
     0.2005979304359007,
     0.2005979304359007,
     0.17504873741057997,
     0.1298104347390131,
     0.0750023262087275,
     0.02227763082733816,
     -0.01822264184977342,
     -0.04035589196521442,
     -0.04321662753179002,
     -0.030837473835488727,
     -0.010534288909074228,
     0.00952630233346234,
     0.022759061611784787,
     0.025865816447546524,
     0.01936333342722582,
     0.006881276659604978,
     -0.006432533785285164,
     -0.01580739054584703,
     -0.018406948697547505,
     -0.01407399531145508,
     -0.005095292414297668,
     0.004841923752344648,
     0.012074103313018496,
     0.014245496416753448,
     0.011021796776966134,
     0.004033290266404478,
     -0.003870294351801647,
     -0.00973756094553485,
     -0.011582979285734997,
     -0.009029385997457956,
     -0.0033271785203400823,
     0.0032132640403633814,
     0.00813273978512545,
     0.00972769699128124,
     0.007622325686837236,
     0.002822258606220101,
     -0.002737940269069003,
     -0.006959029046721823,
     -0.008356875676633322,
     -0.006572654912253929,
     -0.002442166072386912,
     0.0023770620115118202,
     0.006060704811784669,
     0.007299652155009577,
     0.00575723583485291,
     0.0021448625834810824,
     -0.0020929384168351124,
     -0.0053490336766239726,
     -0.006457120692863402,
     -0.0051037209977799905,
     -0.0019052994253283583,
   ]


# Levanto la Imagen de mi Filtro Pasa-Bajos Utilizado:
fp_imagen = './Ejemplo1_Filtro_Digital.jpg'
i = im.open (fp_imagen, 'r')  # Abro la Imagen.
i.show ( ) # Muestro la Imagen en una Ventana.


#%%

# Calculo la Cantidad de Muestras de h[n].
N = len (h) 
 
# Grilla Temporal
t0_h = 0
dt_h = Ts
tf_h = ( N - 1) * dt_h
tt = np.linspace(t0_h, tf_h, N)

# Ploteo de la Señal Filtrada
fig3 = plt.figure ( )
plt.plot (tt, h, 'g')
plt.grid ('true')
plt.title('Respuesta al Impulso del Filtro')
plt.xlabel('$t[seg]$', fontsize = 15)
plt.ylabel('$h(t)$', fontsize = 15)

##############################################################################
##############################################################################

#%% 4) Aplicar el Filtro Diseñado y mostrar la Salida Temporal.

filtered = sig.convolve (h, s)
y = filtered

# Vuelvo a Calular la Cantidad de Muestras una vez calculada la Convolución 
# Discreta.
# El Tamaño de la salida "filtered" (y) va a ser igual a: { la Suma del Tamaño 
# de la Señal de Entrada más el Tamaño o la Cantidad de Muestras de h[n] } - 1
# tamaño (y) = [ tamaño(s) + tamaño/muestras(h) ] - 1
N = len (y) 
 
# Grilla Temporal
t0_y = 0
dt_y = Ts
tf_y = ( N - 1) * dt_y
tt = np.linspace(t0_y, tf_y, N)

# Ploteo de la Señal Filtrada
fig4 = plt.figure ( )
plt.plot (tt, y, 'r')
plt.grid ('true')
plt.title('Señal Filtrada')
plt.xlabel('$t[seg]$', fontsize = 15)
plt.ylabel('$y(t)$', fontsize = 15)


#%%

# Grilla Frecuencial
f0 = 0
df = Fs / N     # Resolución Espectral
ff = (N-1)*df
f = np.linspace(f0, ff, N)

# Calculo la TDF de la Señal Sintetizada Utilizando la FFT:
Y = fft (y)
Abs_Y = np.abs( Y ) / N # Módulo


# Ploteo el Módulo del Espectro de la Señal Filtrada.
fig5 = plt.figure ( )
plt.plot (f, Abs_Y)
plt.title ('Módulo del Espectro de la Señal Filtrada')
plt.grid ('true')
plt.xlabel('$frecuency [Hz]$', fontsize = 13)
plt.ylabel ('$|Y(f)|$', fontsize = 15)


#%% Guardo la Señal Filtrada como un audio de formato .wav

#s = np.uint8 (s)
wavfile.write ('ejemplo1_filtro_digital_out.wav', Fs, s)


#%%

# Ploteo de la Señal de Entrada y la Señal Filtrada.
fig6 = plt.figure ( )
plt.plot (t, s, 'b')
plt.plot (tt, y, 'r')
plt.grid ('true')
plt.title('Señal de Entrada y Señal Filtrada')
plt.legend (['Señal de Entrada', 'Señal Filtrada (Señal de Salida)'])
plt.xlabel('$t[seg]$', fontsize = 15)
plt.ylabel('$f(t)$', fontsize = 15)


##############################################################################
##############################################################################

#%% 5) Calcular la Energía de la Señal en el Tiempo y la Energía de la 
# Respuesta de Módulo.

# Energía de la Señal de Entrada:
N = len(s)
# La calculo como una Señal de Potencia y la Divido por la Cant. de Muestras.
Energ_s_t = np.sum (s**2) / N       

# Energía de la Señal de Salida
N = len (y)
Energ_y_t = np.sum (y**2) / N

# Energía a partir de la Respuesta de Módulo.
Energ_Y_f = np.sum (Abs_Y**2)


# Array con los Valores de las Energía:
Energias = np.array ([Energ_s_t, Energ_y_t, Energ_Y_f])


print ("\n Valores de las Energía: [Energ_s_t, Energ_y_t, Energ_Y_f] : ")
print('\n', Energias)
print('\n')


#%% Relación de Energía entre la Señal de Entrada y Salida:

ratio = Energ_y_t / Energ_s_t
print ("Relación de Energía entre la Señal de Entrada y Salida:  ", ratio)
print ('\n\n\n')