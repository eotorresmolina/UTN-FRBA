# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 20:51:57 2020

@author: Emmanuel Torres Molina
"""

"""
Los sistemas de antenas de transmisión de tipo Phased Array, son un tipo 
particular de antena que permiten controlar la dirección del haz emitido sin 
desplazamientos mecánicos. Se trata en esencia de múltiples antenas que 
reciben la misma señal de entrada, aunque afectada por defasajes diferentes. 
Así, modificando los desfasajes y por efectos de interferencia constructiva o 
destructiva, se logra modificar el ángulo de apuntamiento sin requerir 
desplazamientos mecánicos.
 
Se desea diseñar defasadores pasivos para un sistema de este tipo que opera 
en banda ancha, buscándose que no alteren la respuesta de módulo de la señal.

Ejercicio Nro 1 del desafío del día 08/06/2020:

a) Proponga una función transferencia normalizada de primer orden que permita 
rotar la fase, sin alterar el módulo. Dibuje 1) el diagrama de polos y ceros, 
2) la respuesta de fase en función de la frecuencia y 3) calcule el retardo
de grupo.
 
 
b) Proponga una topología pasiva que implemente el diagrama de 
polos y ceros del punto anterior. Obtenga los valores de componentes pasivos
(resistencias y capacitores) para lograr que la rotación de fase sea de 15º 
en ω=1 (medida respecto de la fase en ω=0).


"""


##############################################################################
##############################################################################

# Importo los Paquetes y Módulos a Utilizar:
    
from splane import bodePlot, pzmap, grpDelay
from scipy.signal import TransferFunction as tf
from scipy import signal as sig
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image as im

plt.close ('all')


##############################################################################
##############################################################################

# Topología Pasiva: Estructura "Lattice":
        
# Valores de los Elementos del Circuito:
R1 = 1  # 10**3
R2 = 0.1316  # 1316
G2 = 1/R2  # Conductancia de R2
C = 1     # 100e-6

K = 0.5

# Valores de los Elementos de la Etapa de Ganancia:
R3 = 1   # 10**3
R4 = R3

K2 = 1 + R4/R2


##############################################################################

# Desarrollo de la Transferencia del Filtro Pasa-Todo o Rotador de Fase 
# Según la Estructura Usada:

NUM = [ 1, -G2/C ]
DEN = [ 1, G2/C ]

# Transferencia Normalizada de mi Filtro Pasa-Todo o Rotador de Fase Pasivo:
my_tf = tf (NUM, DEN)


##############################################################################

# Levanto la Imagen de mi Circuito Pasivo "Lattice" a Utilizar:
fp_imagen = './Circuit_PasaTodo_Pasivo_Lattice.jpg'
i = im.open (fp_imagen, 'r')  # Abro la Imagen.
i.show ( ) # Muestro la Imagen en una Ventana.


##############################################################################

# Ploteo de la Respuesta de Módulo y Respuesta de Fase y el Retardo de Grupo:
bodePlot (my_tf)
pzmap (my_tf)
grpDelay (my_tf)