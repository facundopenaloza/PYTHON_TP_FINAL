#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import random
import string
import clases.casillero as cas
from copy import deepcopy

# Contantes
BOX_SIZE = 25
HORIZONTAL = 'H'
VERTICAL = 'V'
UPPER = 'U'
LOWER = 'L'
VERBOS = 'V'
ADJETIVOS = 'A'
SUSTANTIVOS = 'S'


def grilla_size(cant_palabras, palabra_mas_larga, orientacion=HORIZONTAL):
    """
    El tamaño de la grilla se definirá de acuerdo a la cantidad de
    palabras que la o el docente configuró. Se tomará de referencia la
    longitud de la palabra más larga y la cantidad de palabras.
    
    Args:
        orientacion (str): Indica si la orientación de las palabras es
                           horizontal (H) o vertical (V).
        cant_palabras (int): Cantidad de palabras que contendrá la
                             grilla.
        palabra_mas_larga (int): Largo de la palabra más larga.

    Returns:
        ancho (int): Cantidad de casilleros horizontales.
        alto  (int): Cantidad de casilleros verticales.
    """
    ancho = 0
    alto = 0
    if (orientacion == HORIZONTAL):
        ancho = palabra_mas_larga + 3
        alto = (cant_palabras * 2) - 1
    else:
        alto = palabra_mas_larga + 3
        ancho = (cant_palabras * 2) - 1
    
    return (ancho, alto)


def cargar_matriz(ancho, alto, palabras, orientacion=HORIZONTAL, upper_lower=UPPER):
    lista_casilleros = []
    tipos = [ADJETIVOS, SUSTANTIVOS, VERBOS]
    # palabras = {ADJETIVOS: ['uno', 'tres', 'noventa'], SUSTANTIVOS: ['hola', 'chau', 'no'], VERBOS: ['correr', 'sumar']}
    aux = deepcopy(palabras)

    if (upper_lower == UPPER):
        case = string.ascii_uppercase
    else:
        case = string.ascii_lowercase
        
    # Lista con las posiciones libres
    if (orientacion == HORIZONTAL):
        pos_libres = list(range(0, alto - 1))
    else:
        pos_libres = list(range(0, ancho - 1))

    # Cargo la matriz con letras al azar
    for row in range(alto):
        fila_casilleros = []
        for col in range(ancho):
            letra = random.choice(case)
            casillero = cas.Casillero(col, row, letra)
            fila_casilleros.append(casillero)
            
        lista_casilleros.append(fila_casilleros)

    # Elimino las claves que tengan la lista de palabras vacías
    for k, v in aux.items():
        if (len(v) <= 0):
            del aux[k]
            del tipos[k]

    # Cargo las palabras en la matriz
    while ((len(aux[ADJETIVOS]) > 0)or(len(aux[SUSTANTIVOS]) > 0)or(len(aux[VERBOS]) > 0)):
        # Si hay más de un tipo de palabra, lo selecciono de manera
        # random, sino lo selecciono directamente.
        if (len(aux.keys()) > 1):
            tipo = random.choice(tipos)
        else:
            tipo = aux.keys()[0]
        
        # Dentro del tipo de palabra determinado, selecciono una palabra
        # al azar
        pos = random.randint(0, len(aux[tipo])-1)
        palabra = aux[tipo][pos]
        
        # Obtengo una posición libre al azar (en caso de que la 
        # orientación sea horizontal, obtengo una columna libre y en
        # caso de que sea vertical, obtengo una fila libre.)
        pos_libre = random.choice(pos_libres)
        
        # Determino cuántos casilleros van a tener letras al azar
        if (orientacion == HORIZONTAL):
            # Cantidad de casilleros libres desde la izquierda.
            desplace = random.randint(1, ancho - len(palabra))
            
            cont = 0
            
            # La ubico en la matriz
            for c in palabra:
                lista_casilleros[pos_libre][desplace - 1 + cont].set_letra(c)
                cont += 1
        else:
            # Cantidad de casilleros libres desde arriba.
            desplace = random.randint(1, alto - len(palabra))
            
            cont = 0
            
            # La ubico en la matriz
            for c in palabra:
                lista_casilleros[desplace - 1 + cont][pos_libre].set_letra(c)
                cont += 1
        
        pos_libres.remove(pos_libre)
        aux[tipo].pop(pos)
        
        # Si ya no hay palabras para el tipo seleccionado, lo saco.
        if (len(aux[tipo]) == 0):
            print('pop')
            i = tipos.index(tipo)
            del tipos[i]
        
    print(lista_casilleros)

    return lista_casilleros


def armar_grilla(window, ancho, alto, palabras, orientacion=HORIZONTAL, upper_lower=UPPER):
    """
    Arma la grilla de la Sopa de Letras a partir del ancho y el alto
    
    Args:
        orientacion (str): Indica si la orientación de las palabras es
                           horizontal (H) o vertical (V).
        cant_palabras (int): Cantidad de palabras que contendrá la
                             grilla.
        palabra_mas_larga (int): Largo de la palabra más larga.

    Returns:
        ancho (int): Cantidad de casilleros horizontales.
        alto  (int): Cantidad de casilleros verticales.
    """
    grilla = window.FindElement('_GRAPH_')
    
    lista_casilleros = cargar_matriz(ancho, alto, palabras, orientacion, upper_lower)

    # alto
    for row in range(alto):
        # ancho
        fila_casilleros = []
        for col in range(ancho):
            letra = lista_casilleros[row][col].get_letra()
            grilla.DrawRectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color='white')
            letter_location = (col * BOX_SIZE + 18, row * BOX_SIZE + 17)
            
            grilla.DrawText('{}'.format(letra), letter_location, font='Courier 25')
            

    return (grilla, lista_casilleros)


def validar_sopa(lista_casilleros, pal_seleccionadas, cant_palabras, orientacion, adje_color, sust_color, verb_color):
    
    alto = len(lista_casilleros)
    ancho = len(lista_casilleros[0])
    resultado = {}
    cant_adje_bien = 0
    cant_sust_bien = 0
    cant_verb_bien = 0
    
    
    if (orientacion == HORIZONTAL):

        for row in range(alto):
            pal = ''
            color_set = set()
            for col in range(ancho):
                if (lista_casilleros[row][col].esta_seleccionado()):
                    pal = pal + lista_casilleros[row][col].get_letra()
                    color_set.add(lista_casilleros[row][col].get_color())
            
            print('len', len(color_set))
            print('pal', pal)
            # Verifico que la palabra esté pintada del mismo color.
            # Sino no la tengo en cuenta.
            if (len(color_set) == 1):
                
                # Obtengo el color del set
                for c in color_set:
                    color = c
                
                print(pal, color)
                if ((pal in pal_seleccionadas[ADJETIVOS])and(color == adje_color)):
                    cant_adje_bien += 1
                elif ((pal in pal_seleccionadas[SUSTANTIVOS])and(color == sust_color)):
                    cant_sust_bien += 1
                elif ((pal in pal_seleccionadas[VERBOS])and(color == verb_color)):
                    cant_verb_bien += 1
    
    elif (orientacion == VERTICAL):

        for col in range(ancho):
            pal = ''
            color_set = set()
            for row in range(alto):
                if (lista_casilleros[row][col].esta_seleccionado()):
                    pal = pal + lista_casilleros[row][col].get_letra()
                    color_set.add(lista_casilleros[row][col].get_color())
            
            print('len', len(color_set))
            print('pal', pal)
            # Verifico que la palabra esté pintada del mismo color.
            # Sino no la tengo en cuenta.
            if (len(color_set) == 1):
                
                # Obtengo el color del set
                for c in color_set:
                    color = c
                
                print(pal, color)
                if ((pal in pal_seleccionadas[ADJETIVOS])and(color == adje_color)):
                    cant_adje_bien += 1
                elif ((pal in pal_seleccionadas[SUSTANTIVOS])and(color == sust_color)):
                    cant_sust_bien += 1
                elif ((pal in pal_seleccionadas[VERBOS])and(color == verb_color)):
                    cant_verb_bien += 1

            
    if (cant_adje_bien < len(pal_seleccionadas[ADJETIVOS])):
        print('Faltan adjetivos.')
        resultado[ADJETIVOS] = {'ok': False, 'info': 'No se encontraron todos los Adjetivos o fueron mal clasificados.'}
    elif (cant_adje_bien > len(pal_seleccionadas[ADJETIVOS])):
        print('Hay adjetivos de más.')
        resultado[ADJETIVOS] = {'ok': False, 'info': 'Se marcaron Adjetivos de más.'}
    else:
        print('Adjetivos correctos.')
        resultado[ADJETIVOS] = {'ok': True, 'info': 'Adjetivos correctos.'}
    
    if (cant_sust_bien < len(pal_seleccionadas[SUSTANTIVOS])):
        print('Faltan sustantivos.')
        resultado[SUSTANTIVOS] = {'ok': False, 'info': 'No se encontraron todos los Sustantivos o fueron mal clasificados.'}
    elif (cant_sust_bien > len(pal_seleccionadas[SUSTANTIVOS])):
        print('Hay sustantivos de más.')
        resultado[SUSTANTIVOS] = {'ok': False, 'info': 'Se marcaron Sustantivos de más.'}
    else:
        print('Sustantivos correctos.')
        resultado[SUSTANTIVOS] = {'ok': True, 'info': 'Sustantivos correctos.'}
        
    if (cant_verb_bien < len(pal_seleccionadas[VERBOS])):
        print('Faltan verbos.')
        resultado[VERBOS] = {'ok': False, 'info': 'No se encontraron todos los Verbos o fueron mal clasificados.'}
    elif (cant_verb_bien > len(pal_seleccionadas[VERBOS])):
        print('Hay verbos de más.')
        resultado[VERBOS] = {'ok': False, 'info': 'Se marcaron Verbos de más.'}
    else:
        print('Verbos correctos.')
        resultado[VERBOS] = {'ok': True, 'info': 'Verbos correctos.'}

    return (resultado)
