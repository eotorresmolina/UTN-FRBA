# -*- coding: utf-8 -*-
"""
Created on Thu May 28 21:28:44 2020

@author: Emmanuel Torres Molina
"""

"""
Script con una Introducción y los primeros pasos de la Computación Simbólica a 
través del Paquete Sympy de Python.

"""

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

# Importo todos los módulos que voy a utilizar:
from sympy import init_session
init_session (use_latex = True) # Activo las Impresiones con Latex
from sympy import *


# ----------------------------------------------------------------------------

# Si quiero una Variable como "Símbolo" primero debo crearla como tal.
# Las Variables de tipo "Symbols" actúan como contenedores en lo que no sabemos
# que hay (un real, un complejo, una lista, etc.)
# Hay que tener en cuenta que una cosa es el nombre de la variable y otra el 
# símbolo con el que se representa.
# NOTA: Las Operaciones con Símbolos devuelven Símbolos y/o Expresiones.
# Creo 2 Variables Simbólicas
a, b = symbols ('a, b')

# c no es una Variable Simbólica sino que es un variable del tipo "potencia"
c = (a + b) ** 2

# d es una Variable Compleja: para denotar un numero imaginario usamos "I" (Mayúscula)
d = 2 + 4 * I

# f tiene el valor de e que se denota con "E" (Mayúscula)
f = E


# ----------------------------------------------------------------------------

# 2 Variables Símbolicas que van a Ser Impresas en Latex:
alpha, beta = symbols ('alpha, beta')

# Varible Simbólica con Subíndice:
tau_s = symbols ('tau_s')

# Accedo a las Restriciones de un Símbolo a través de la Propiedad "assumptions0" 
# Permite ver las "restricciones" de dicho símbolo.
alpha.assumptions0

# Defino nuevamente una variable simbólica, y le doy nuevas "propiedades"
x = symbols ('x', real = True, positive = True)
x.assumptions0


# ----------------------------------------------------------------------------

# Creación de Expresiones:
z = symbols ('z')
sin(z)**2 + cos(z)**2

# Simplifico dicha Expresión Anterior con la Función: "simplify ( )"
simplify ( sin(z)**2 + cos(z)**2 ) # Obviamente devuelve 1


# Ahora si hago lo siguiente:
z = symbols ('z')
simplify ( sqrt(z**2) ) # Me va devolver sqrt (z**2)

# Pero si ahora le agrego una propiedad a Z:
z = symbols ('z', real = True)

# Me va a devolver el Módulo de z: |z|, si le hubiese especificado que z era
# también real solo me devolvería z
simplify ( sqrt(z**2) ) 


# Sustituyo una Variable Simbólica por Otra Variable o Expresión Simbólica:
# Uso la función "subs ( )"
a = sin(z)**2 + cos(z)**2 # a le asigno esa expresión simbólica.
b = a.subs (z, x**2 + 1)

# Si quiero Sustituir varias variables simbólicas:
x, y, z = symbols ('x, y, z')
h = sin(x)**2 + cos(y)**2
# Uso un Diccionario.
h.subs ({x: 1+z, y: 1-z })


# Si ahora quiero cambiar una Expresión Simbólica por otra, uso la función:
# "replace ( )":
g = sin (z)
p = g.replace (sin, exp) # Cambio la función seno por una función exponencial.

# Si cambio una variable simbólica por un valor específico utilizo también la
# función "subs ( )"
k = g.subs (z, pi/2)


# Ahora si quiero obtener el valor numérico de una variable simbólica, utilizo
# lo mejor es utilizar la función "evalf ( )"
t = 3 * pi
y = t.evalf ( )

# La función "N ( )" realiza también lo mismo que "evalf ( )".
w = N(t)