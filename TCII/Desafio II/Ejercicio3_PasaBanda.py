# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 21:09:35 2020

@author: Emmanuel Torres Molina
"""

"""

Ejercicio Nro 3 del desafío del día 08/06/2020:

3) Dada la Siguiente Respuesta de Fase: 
    phi (w) = pi/2 - arctg ( -6w / (-w^2 + 4) )

Obtener la expresión de F(s)  ==> F($) = $ / ( $^2 + 6$ + 4 ) (Se obtuvo a Mano)
Graficar el diagrama de polos y ceros, y con el mismo, verificar la respuesta 
de fase en extremos de banda
Obtener un circuito equivalente pasivo que implemente dicha respuesta


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

# Topología Pasiva:
        
# Valores de los Elementos del Circuito:
R1 = 0.25  # 2500
R2 = 1  # 10**3
C1 = 1  # 100e-6
C2 = C1     # 100e-6


##############################################################################

# Desarrollo de la Transferencia del Filtro Pasa-Banda Pasivo Según la 
# Estructura Usada:

NUM = [ 1/R2*C2, 0 ]
DEN = [ 1, (1/(C1*R2) + 1/(C1*R1) + 1/(C2*R2)), 1/(R1*R2*C1*C2) ]

# Transferencia Normalizada de mi Filtro Pasa-Banda Pasivo:
my_tf = tf (NUM, DEN)


##############################################################################

# Levanto la Imagen de mi Circuito Pasivo a Utilizar:
fp_imagen = './Circuito_Ejercicio3_PasaBanda.jpg'
i = im.open (fp_imagen, 'r')  # Abro la Imagen.
i.show ( ) # Muestro la Imagen en una Ventana.


##############################################################################

# Ploteo de la Respuesta de Módulo y Respuesta de Fase y el Retardo de Grupo:
bodePlot (my_tf)
pzmap (my_tf)
grpDelay (my_tf)