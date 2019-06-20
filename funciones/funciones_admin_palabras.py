#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import json
import random
from wiktionaryparser import WiktionaryParser

VERBOS = 'V'
ADJETIVOS = 'A'
SUSTANTIVOS = 'S'
UPPER = 'U'
LOWER = 'L'
NOMBRE_ARCHIVO = 'palabras.txt'

def leer_palabras_archivo(window):

    adjetivos=[]
    sustantivos=[]
    verbos=[]
    
    try:

        with open(NOMBRE_ARCHIVO) as json_file:
            data = json.load(json_file)
            
            adje = window.FindElement('_ADJE_LIST_')
            sust = window.FindElement('_SUST_LIST_')
            verb = window.FindElement('_VERB_LIST_')
            
            if (ADJETIVOS in data):
                adje.Update(values=data[ADJETIVOS])
                adjetivos = data[ADJETIVOS][:]
            
            if (SUSTANTIVOS in data):
                sust.Update(values=data[SUSTANTIVOS])
                sustantivos = data[SUSTANTIVOS][:]
            
            if (VERBOS in data):
                verb.Update(values=data[VERBOS])
                verbos = data[VERBOS][:]
                
        return adjetivos, sustantivos, verbos
        
    except (FileNotFoundError, IOError, OSError):
        sg.Popup('Atención', 'No existe el archivo de palabras o hay un error en la ruta.')
        return [], [], []
    except (PermissionError):
        sg.Popup('Atención', 'No cuenta con permisos para abrir el archivo de palabras.')
        return [], [], []
    except (EOFError):
        sg.Popup('Atención', 'Se excedió en la lectura del archivo.')
        return [], [], []
    except ValueError:
        sg.Popup('Atención', 'Error en el formato del archivo.')
        return [], [], []
    except:
        sg.Popup('Atención', 'Error al abrir el archivo.')
        return [], [], []


def obtener_tipo_palabra(palabra):
    """
    Valida que la palabra exista. En caso afirmativo, retorna el tipo
    de palabra (Adjetivo, sustantivo o verbo). Caso negativo, retorna
    vacío.
    
    Args:
        palabra (str): Palabra a validar.

    Returns:
        Tipo (str): Tipo de palabra, siendo estos 'A' para Adjetivo,
                    'S' para Sustantivo y 'V' para Verbo.
                    En caso de que la palabra no exista, retorna vacío.
    """
    
    try:

        parser = WiktionaryParser()
        parser.set_default_language('spanish')

        word = parser.fetch(palabra)

        tipo_palabra = word[0]['definitions'][0]['partOfSpeech']
        
        if (tipo_palabra == 'adjective'):
            return(ADJETIVOS)
        elif (tipo_palabra == 'noun'):
            return(SUSTANTIVOS)
        elif (tipo_palabra == 'verb'):
            return(VERBOS)
        else:
            return('')
    
    except IndexError:
        return('')


def agregar_palabras(palabra, window, adjetivos, sustantivos, verbos):
    
    adje = window.FindElement('_ADJE_LIST_')
    sust = window.FindElement('_SUST_LIST_')
    verb = window.FindElement('_VERB_LIST_')
    
    if (palabra != ''):
    
        tipo = obtener_tipo_palabra(palabra)
        
        if (tipo != ''):
            if (tipo == ADJETIVOS):
                if (not palabra.upper() in adjetivos):
                    adjetivos.append(palabra.upper())
                    adje.Update(values=adjetivos)
                    window.FindElement('_PAL_').Update('')
                elif (palabra.upper() in adjetivos):
                    sg.Popup('Error', 'La palabra ' + palabra.upper() + ' ya fue agregada.')
            elif (tipo == SUSTANTIVOS):
                if (not palabra.upper() in sustantivos):
                    sustantivos.append(palabra.upper())
                    sust.Update(values=sustantivos)
                    window.FindElement('_PAL_').Update('')
                elif (palabra.upper() in sustantivos):
                    sg.Popup('Error', 'La palabra ' + palabra.upper() + ' ya fue agregada.')
            elif (tipo == VERBOS):
                if (not palabra.upper() in verbos):
                    verbos.append(palabra.upper())
                    verb.Update(values=verbos)
                    window.FindElement('_PAL_').Update('')
                elif (palabra.upper() in verbos):
                    sg.Popup('Error', 'La palabra ' + palabra.upper() + ' ya fue agregada.')
            else:
                sg.Popup('Error', 'La palabra ' + palabra.upper() + ' no es adjetivo, sustantivo o verbo.')
        else:
            sg.Popup('Error', 'La palabra ' + palabra.upper() + ' no es válida.')
            
    else:
        sg.Popup('Atención', 'Ingrese una palabra.')


def borrar_palabras(palabra, window, adjetivos, sustantivos, verbos):
    
    adje = window.FindElement('_ADJE_LIST_')
    sust = window.FindElement('_SUST_LIST_')
    verb = window.FindElement('_VERB_LIST_')
    
    if (palabra != ''):
        if (palabra in adjetivos):
            adjetivos.remove(palabra.upper())
            adje.Update(values=adjetivos)
            window.FindElement('_PAL_').Update('')
        elif (palabra in sustantivos):
            sustantivos.remove(palabra.upper())
            sust.Update(values=sustantivos)
            window.FindElement('_PAL_').Update('')
        elif (palabra in verbos):
            verbos.remove(palabra.upper())
            verb.Update(values=verbos)
            window.FindElement('_PAL_').Update('')
        else:
            sg.Popup('Error', 'La palabra ' + palabra.upper() + ' no se encuentra en ninguna lista.')
    else:
        sg.Popup('Atención', 'Ingrese una palabra.')


def guardar_cambios(adjetivos, sustantivos, verbos):
    try:
        with open(NOMBRE_ARCHIVO, 'w') as json_file:
            data = {ADJETIVOS: adjetivos, SUSTANTIVOS: sustantivos, VERBOS: verbos}
            json.dump(data, json_file)
        
        return True

    except (FileNotFoundError, IOError, OSError):
        sg.Popup('Atención', 'No existe el archivo de palabras o hay un error en la ruta.')
        return False
    except (PermissionError):
        sg.Popup('Atención', 'No cuenta con permisos para abrir el archivo de palabras.')
        return False
    except ValueError:
        sg.Popup('Atención', 'Error en el formato del archivo.')
        return False
    except:
        sg.Popup('Atención', 'Error al abrir el archivo.')
        return False


def administrar_palabras():
    layout_admin = [
        [sg.Listbox(values=(), key='_ADJE_LIST_', size=(30, 10)), sg.Text('Adjetivos')],
        [sg.Listbox(values=(), key='_SUST_LIST_', size=(30, 10)), sg.Text('Sustantivos')],
        [sg.Listbox(values=(), key='_VERB_LIST_', size=(30, 10)), sg.Text('Verbos')],
        [
            sg.Text('Palabra a agregar:', size=(15, 1)),
            sg.InputText('', key='_PAL_'),
            sg.Button('Agregar'),
            sg.Button('Borrar')
        ],
        [sg.Button('Guardar'), sg.Button('Cancelar')]
    ]
    
    layout_confirma = [
        [sg.Text('¿Desea descartar los cambios realizados?')],
        [sg.Button('SI'), sg.Button('NO')]
    ]

    adjetivos=[]
    sustantivos=[]
    verbos=[]

    window_ap = sg.Window('Administrador de palabras', default_element_size=(40, 1), grab_anywhere=False, ).Layout(layout_admin).Finalize()

    adjetivos, sustantivos, verbos = leer_palabras_archivo(window_ap)
    
    button, values = window_ap.Read()

    # Agrega y elimina palabras hasta que presiona el botón Guardar
    # o Cancelar
    while ((button != 'Guardar')and(button != 'Cancelar')):
        if (button == 'Agregar'):
            agregar_palabras(values['_PAL_'], window_ap, adjetivos, sustantivos, verbos)

        elif (button == 'Borrar'):
            borrar_palabras(values['_PAL_'], window_ap, adjetivos, sustantivos, verbos)
            
        button, values = window_ap.Read()
        
        # Si presionó el botón Cancelar, solicito una confirmación,
        # para asegurarme de que quiere descartar los cambios.
        if (button == 'Cancelar'):
            w_confirma = sg.Window('Atención!').Layout(layout_confirma)
            button_conf, values_conf = w_confirma.Read()
            if (button_conf == 'NO'):
                button = ''
                continue
    
    if (button == 'Guardar'):
        result = guardar_cambios(adjetivos, sustantivos, verbos)
        
        if (result):
            sg.Popup('Éxito', 'Modificaciones guardadas exitosamente.')
        else:
            sg.Popup('Atención', 'Error al guardar los cambios.')

    window_ap.Close()

def seleccionar_adjetivos(adjetivos, cant_adj=0):
    """
    Se elegirán aleatoriamente, tantos adjetivos como se hayan
    solicitado.
    
    Args:
        adjetivos (list): Lista de adjetivos cargada desde el archivo.
        cant_adj (int): Cantidad de adjetivos que se seleccionarán
                        para integrar la grilla.

    Returns:
        lista (list): Retorna la lista de palabras con la cantidad de
                      elementos solicitados.
    """

    if (cant_adj > 0):
        if (len(adjetivos) > cant_adj):
            adj = adjetivos[:]
            lista = []
            while (True):
                pos = random.randint(0, len(adj)-1)
                if (not adj[pos] in lista):
                    lista.append(adj[pos])
                    del adj[pos]
                    if (len(lista) == cant_adj):
                        return (lista)
        else:
            # En caso de que haya menos palabras que las solicitadas
            return(adjetivos)
    else:
        return([])


def seleccionar_sustantivos(sustantivos, cant_sust=0):
    """
    Se elegirán aleatoriamente, tantos sustantivos como se hayan
    solicitado.
    
    Args:
        sustantivos (list): Lista de sustantivos cargada desde el
                            archivo.
        cant_sust (int): Cantidad de sustantivos que se seleccionarán
                         para integrar la grilla.

    Returns:
        lista (list): Retorna la lista de palabras con la cantidad de
                      elementos solicitados.
    """

    if (cant_sust > 0):
        if (len(sustantivos) > cant_sust):
            sust = sustantivos[:]
            lista = []
            while (True):
                pos = random.randint(0, len(sust)-1)
                if (not sust[pos] in lista):
                    lista.append(sust[pos])
                    del sust[pos]
                    if (len(lista) == cant_sust):
                        return (lista)
        else:
            # En caso de que haya menos palabras que las solicitadas
            return(sustantivos)
    else:
        return([])



def seleccionar_verbos(verbos, cant_verbos=0):
    """
    Se elegirán aleatoriamente, tantos verbos como se hayan solicitado.
    
    Args:
        verbos (list): Lista de verbos cargada desde el archivo.
        cant_verbos (int): Cantidad de verbos que se seleccionarán
                           para integrar la grilla.

    Returns:
        lista (list): Retorna la lista de palabras con la cantidad de
                      elementos solicitados.
    """
    
    if (cant_verbos > 0):
        if (len(verbos) > cant_verbos):
            verb = verbos[:]
            lista = []
            while (True):
                pos = random.randint(0, len(verb)-1)
                if (not verb[pos] in lista):
                    lista.append(verb[pos])
                    del verb[pos]
                    if (len(lista) == cant_verbos):
                        return (lista)
        else:
            # En caso de que haya menos palabras que las solicitadas
            return(verbos)
    else:
        return([])


def seleccionar_palabras(cant_adj=0, cant_sust=0, cant_verb=0, upper_lower=UPPER):
    """
    Se elegirán aleatoriamente del conjunto de palabras tantos
    sustantivos, verbos y adjetivos como se hayan configurado
    
    Args:
        cant_adj (int): Cantidad de adjetivos que se seleccionarán
                        para integrar la grilla.
        cant_sust (int): Cantidad de sustantivos que se seleccionarán
                         para integrar la grilla.
        cant_ver (int): Cantidad de verbos que se seleccionarán
                        para integrar la grilla.

    Returns:
        palabras (dict): Diccionario que contiene las claves
                         'V' (verbos), 'S' (sustantivos) y
                         'A' (adjetivos) y por cada una de estas hay
                         una lista con sus respectivas palabras.
    """
    
    seleccionadas = {ADJETIVOS: [], SUSTANTIVOS: [], VERBOS: []}
    
    
    try:

        with open(NOMBRE_ARCHIVO) as f:
            palabras = json.load(f)
            
            if (ADJETIVOS in palabras):
                seleccionadas[ADJETIVOS] = seleccionar_adjetivos(palabras[ADJETIVOS], cant_adj)
            else:
                seleccionadas[ADJETIVOS] = []
            
            if (SUSTANTIVOS in palabras):
                seleccionadas[SUSTANTIVOS] = seleccionar_sustantivos(palabras[SUSTANTIVOS], cant_sust)
            else:
                seleccionadas[SUSTANTIVOS] = []
            
            if (VERBOS in palabras):
                seleccionadas[VERBOS] = seleccionar_verbos(palabras[VERBOS], cant_verb)
            else:
                seleccionadas[VERBOS] = []
        
        for k, v in seleccionadas.items():
            if (upper_lower == UPPER):
                seleccionadas[k] = [x.upper() for x in v]
            else:
                seleccionadas[k] = [x.lower() for x in v]
                
        
        return (seleccionadas)
        
    except (FileNotFoundError, IOError, OSError):
        sg.Popup('Atención', 'No existe el archivo de palabras o hay un error en la ruta.')
        return ({ADJETIVOS: [], SUSTANTIVOS: [], VERBOS: []})
    except (PermissionError):
        sg.Popup('Atención', 'No cuenta con permisos para abrir el archivo de palabras.')
        return ({ADJETIVOS: [], SUSTANTIVOS: [], VERBOS: []})
    except (EOFError):
        sg.Popup('Atención', 'Se excedió en la lectura del archivo.')
        return ({ADJETIVOS: [], SUSTANTIVOS: [], VERBOS: []})
    except ValueError:
        sg.Popup('Atención', 'Error en el formato del archivo.')
        return ({ADJETIVOS: [], SUSTANTIVOS: [], VERBOS: []})
    except:
        sg.Popup('Atención', 'Error al abrir el archivo.')
        return ({ADJETIVOS: [], SUSTANTIVOS: [], VERBOS: []})

