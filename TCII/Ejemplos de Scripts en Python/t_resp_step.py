# -*- coding: utf-8 -*-
"""
Created on Wed May 20 18:46:39 2020

@author: Emmanuel Torres Molina 
"""

"""
Funciones que Calculan Parámetros Característicos de la Respuesta Temporal 
cuando en la Entrada Inyecto una "Señal Escalón"

Incluye También una función que me genera una Señal Escalón, pero no la plotea.

Creo que los valores devueltos por las funciones dependen mucho de la cantidad
de Muestras que se va a Tomar y de la Fs (Frecuencia de Muestreo) utilizada.

"""


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------


import matplotlib.pyplot as plt
import numpy as np
from scipy import signal as sig

plt.close ('all')

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------


"""
Unit Step Function:
      
    u = 0 ,     t < 0
    u = 1,      t >= 0

"""
def esc(t):
    
    # Function defined for parts.
    u = np.piecewise (t, [t<0, t>=0], [lambda t: 0, lambda t: 1])
    
    return u


# ----------------------------------------------------------------------------


# tr: Tiempo de Subida. Tiempo que tarda en alcanzarse el primer cruce de la 
# respuesta con el valor de estabilización del sistema desde que se aplicó en
# la entrada una Señal "Escalón".
# ATENCION: Se suele utilizar para Sistemas "Subarmotigüados".
# Se calcula aprox. el 99.9% del valor final (valor de estabilizacion)
# return: time rise, Response Value(tr), Percentage time rise
def rise_time (t = None, step_resp = None):
    
    if t is None:
        tr = np.array ( [ ] )
        mod_tr = np.array ( [ ] )
        percent_tr = np.array ( [ ] )
        
    else:
        if step_resp is None:
            tr = np.array ( [ ] )
            mod_tr = np.array ( [ ] )
            percent_tr = np.array ( [ ] )
            
        else:
            val = 0.999 * step_resp[-1]
            aux = np.flatnonzero ( step_resp >= val )
            tr = t [ aux[0] ]
            mod_tr = step_resp [ aux[0] ]
            percent_tr = ( step_resp [aux[0]] - step_resp[-1] ) * 100
            
        
    return tr, mod_tr, percent_tr


# ----------------------------------------------------------------------------


# Función que Calcula el "Tiempo que tarda en alcanzar el Pico Máximo 
# Máximo SobreImpulso y su Magnitud, y la SO: SobreOscilacion."
# SO: Relación Porcentual del valor de la salida de un sistema ante una entrada
#     Escalón para el instante en el que se alcanza el 1er Máximo, respecto al
#     valor de estabilización de la respuesta.
# return: time speak, Maximum Peak.
def peak_time_mag (t = None, step_resp = None):
    
    if t is None: 
        time_speak = np.array ( [ ] )        
        max_peak = np.array ( [ ] )
        so_ts = np.array ( [ ] )
             
    else:
        if step_resp is None:
            time_speak = np.array ( [ ] )        
            max_peak = np.array ( [ ] )
            so_ts = np.array ( [ ] )
        
        else:
               max_peak = np.max(step_resp)
               tp = np.where (step_resp == max_peak)
               tp = np.array(tp)
               time_peak = t[tp[0,0]]
               so_ts = ( max_peak - step_resp[-1] ) * 100
        
    
    return time_peak, max_peak, so_ts


# ----------------------------------------------------------------------------


# Función que Calcula el "Tiempo que tarda en alcanzar aprox. el 2% del valor 
# final, y el Porcentaje"
# return: time settling, Percentage time settling, Module Value
def settling_time_step_resp (t = None, step_resp = None):
    
    if t is None:      
        ts = np.array ( [ ] )
        percent_ts = np.array ( [ ] )
        val_mod = np.array ( [ ] )
        
    else:
        if step_resp is None:
            ts = np.array ( [ ] )
            percent_ts = np.array ( [ ] )
            val_mod = np.array ( [ ] )
            
        else:
            # Maximum Tolerance: 2%
            max_k = 0.98 * step_resp[-1]
            aux = np.flatnonzero ( step_resp <= max_k )
            ts = t [ aux[-1] ]
            percent_ts = ( step_resp[-1] - step_resp[ aux[-1] ] ) * 100
            val_mod = step_resp [ aux[-1] ]
    

    return ts, percent_ts, val_mod


# ----------------------------------------------------------------------------


# Función que Devuelve el tiempo y la Salida cuando la Entrada es un Señal
# Escalón en función del factor de amortigüamiento pasado como parámetro. 
# La Pulsación Angular y Amplitud del Escalón también se puede pasar 
# como parámetro.
# ATENCIÓN: ESTA FUNCIÓN FUE IMPLEMENTADA EN BASE A UN FILTRO PASA-BAJOS
# DE SEGUNDO ORDEN.
#               w0^2
#       ---------------------
#        $^2 + $*2*w0 + w0^2
# return: time, y_output
def step_resp_SecondOrder (t = None, fact_amort = None, w0 = None, Amp = None):
    
    if t is None:
        tt = np.array ( [ ] )
        y_out = np.array ( [ ] )
        
    else:
        if fact_amort is None:
                    tt = np.array ( [ ] )
                    y_out = np.array ( [ ] )
                    
        else:
            if w0 is None:  # w0 = 1 [rad/seg] "Normalizado"
               NUM = [1]
               DEN = [1, 2*fact_amort*1, 1]
               
            else:
                z = np.array ( [ ] )
                p = np.roots ( [1, 2*fact_amort*w0, w0**2] )
                k = w0**2
                NUM, DEN = sig.zpk2tf (z, p, k)
                
                if Amp is None:
                     u = 1 * esc(t)
                     
                else:
                     u = Amp * esc(t)
    
    
                tt, y_out, x = sig.lsim2 ( (NUM, DEN), u, t )
    
    
    return tt, y_out             


# Función que Devuelve el tiempo y la Salida cuando la Entrada es un Señal
# Escalón en función del Q: Factor de Selectividad pasado como parámetro. 
# La Pulsación Angular y Amplitud del Escalón también se puede pasar 
# como parámetro.
# ATENCIÓN: ESTA FUNCIÓN FUE IMPLEMENTADA EN BASE A UN FILTRO PASA-BAJOS
# DE SEGUNDO ORDEN.
#               w0^2
#       ---------------------
#        $^2 + $*(w0/Q) + w0^2
# return: time, y_output
def step_resp_SecondOrder2 (t = None, Q = None, w0 = None, Amp = None):
    
    if t is None:
        tt = np.array ( [ ] )
        y_out = np.array ( [ ] )
        
    else:
        if Q is None:
                    tt = np.array ( [ ] )
                    y_out = np.array ( [ ] )
                    
        else:
            if w0 is None:  # w0 = 1 [rad/seg] "Normalizado"
               NUM = [1]
               DEN = [1, 1/Q, 1]
               
            else:
                z = np.array ( [ ] )
                p = np.roots ( [1, w0/Q, w0**2] )
                k = w0**2
                NUM, DEN = sig.zpk2tf (z, p, k)
                
                if Amp is None:
                     u = 1 * esc(t)
                     
                else:
                     u = Amp * esc(t)
    
    
                tt, y_out, x = sig.lsim2 ( (NUM, DEN), u, t )
    
    
    return tt, y_out             