# -*- coding: utf-8 -*-
"""
Created on Sun May 10 23:28:47 2020

@author: Emmanuel Torres Molina
"""

"""
Desarrollo de la Señal Escalón

"""

import numpy as np

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

# Defino la Señal "Escalón Unitario" a través de la función piecewise.
"""
Unit Step Function:
      
    u = 0 ,     t < 0
    u = 1,      t >= 0

"""
def esc(t):
    
    # Function defined for parts.
    u = np.piecewise (t, [t<0, t>=0], [lambda t: 0, lambda t: 1])
    
    return u



