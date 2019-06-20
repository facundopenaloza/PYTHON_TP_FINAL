#!/usr/bin/env python
# -*- coding: utf-8 -*-


VERBOS = 'V'
ADJETIVOS = 'A'
SUSTANTIVOS = 'S'

def palabra_mas_larga(palabras={}):
    """
    De la lista de palabras, determina la palabra de mayor longitud.
    
    Args:
        palabras (dict): Diccionario que contiene las claves
                         'V' (verbos), 'S' (sustantivos) y
                         'A' (adjetivos) y por cada una de estas hay
                         una lista con sus respectivas palabras.

    Returns:
        longitud (str): Longitud de la palabra más larga.
    """
    
    palabra = ''
    longitud = 0
    
    for k, v in palabras.items():
        for pal in v:
            if (len(pal) > longitud):
                palabra = pal
                longitud = len(pal)

    return (longitud)


def asignar_color(color):
    if (color == 'Rojo'):
        return ('red')
    elif (color == 'Azul'):
        return ('blue')
    elif (color == 'Verde'):
        return ('green')
    else:
        return ('yellow')
